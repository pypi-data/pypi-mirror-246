/*
 *  AX LC Hub Node
 *
 *  🟣 $HOME/repos/ax/devapps/lc-python/docs/dev/devnotes/hub.md
 */
const NRH = process.env.NODE_RED_HOME;
const projects = require(`${NRH}/../@node-red/runtime/lib/api/projects`);
const flows = require(`${NRH}/../@node-red/runtime/lib/api/flows`);
//var http = require('/opt/conda/lib/node_modules/node-red/node_modules/@node-red/nodes/core/network/21-httpin')
const fs = require('fs');

function rebuild_all_flows(AH, RED, g) {
  let n;
  AH.RED = RED;
  AH.object_cache = undefined;
  AH.supported_ax_exit_nodes = {};
  AH.entry_nodes_checked_for_ax_wires_in = {};
  AH.ax_ops_no_send = {};
  flows
    .getFlows({
      req: null
    })
    .then((v) => {
      let a;
      AH.all_flows = a = v;
      AH.by_id = {};
      AH.all_ax_ops = {};
      for (let i = 0; i < a.flows.length; i++) {
        n = a.flows[i];
        AH.by_id[n.id] = n;
        if (is_ax(n)) {
          AH.all_ax_ops[n.id] = n;
        }
      }

      AH.dyn_snks = find_dyn_snks(AH, RED, g);
    });
}

function is_ax(n) {
  if (!n) return; // unknown nodes, e.g. testnode must work in tests
  const t = n.type;
  if (t.split('ax-')[0] !== '' && t !== 'ax-hub' && t !== 'ax-src') return true;
}

function dyn_snk_ws_out(hub, RED, _g, snk) {
  /* when a dyn snk sees a subs change we must potentially inform all clients */
  const srv = RED.nodes.getNode(snk.server);
  srv.on('opened', function (event) {
    hub.$hub_msgs.next({
      msg: {
        type: 'subs_change',
        connected: event.count,
        node: snk.id,
        mode: 'subscribed'
      }
    });
    console.log('open', event.count);
  });
  srv.on('closed', function (event) {
    hub.$hub_msgs.next({
      msg: {
        type: 'subs_change',
        connected: event.count,
        node: snk.id,
        mode: 'unsubscribed'
      }
    });
    console.log('open', event.count);
  });
}
// Node snks which are sometimes subscribed, sometimes not:
const on_sub_change_by_dyn_snk_type = {
  'websocket out': dyn_snk_ws_out
};

function find_dyn_snks(AH, RED, g) {
  AH.dyn_snk_types = Object.keys(on_sub_change_by_dyn_snk_type);
  const dyn_snks = {};
  for (const [id, snk] of Object.entries(AH.by_id)) {
    if (snk.wires && snk.wires.length === 0) {
      const on_subs_change = on_sub_change_by_dyn_snk_type[snk.type];
      if (on_subs_change) {
        dyn_snks[id] = 'unsubscribed';
        on_subs_change(AH, RED, g, snk);
      }
    }
  }
  return dyn_snks;
}

function ax_make_hub(node, g, RED) {
  /* at every redeploy/startup*/
  const nodes = RED.nodes;
  const newid = () => {
    /* generates short fast ids */
    const i = () => Math.random().toString(36).substring(2, 10);
    return `ax-${i()}-${i()}`;
  };

  const js = JSON.stringify;
  const jp = JSON.parse;
  // settings.json: our utility libs:
  const ws = g.ws;
  const Rx = g.Rx;
  const rx = g.rx;
  const log = console.log;

  function to_binary(msg) {
    /*
     * We do the reverse operation than in from_binary
     * Pop payload, dumps the rest, concat:
     */
    let hl;
    const pl = msg.payload;
    //return pl
    // TODO: pop payload from *any* msg
    const head = JSON.stringify({
      type: msg.type,
      enc: msg.enc,
      pll: pl.length,
      func: msg.func,
      ts: msg.ts,
      _ids: msg._ids
    });
    hl = `0000${head.length}`;
    hl = hl.substr(hl.length - 5);

    const buf = Buffer.from(hl + head, 'utf-8');
    return Buffer.concat([buf, pl]);
  }

  function from_binary(b) {
    /* Binary data sent by the client, usually msgpack in lz4.
     * Done for large chunks after e.g. buffer_with_time
     * We do not unpack but forward to the next python client, just need the header
     * here.
     * Proto:
     * python side:
     * head = dumps(msg).encode('utf-8')
     * m = bytes('%s|%s|' % (enc, len(head)), 'utf-8') + head + pl
     * ord('|') is 124
     */

    let lh;
    let m;
    try {
      lh = parseInt(b.toString('utf-8', 0, 5));
      m = b.toString('utf-8', 5, 5 + lh);
      m = jp(m);
      // not needed, we are not stream decoding, have msgs to the end:
      //'pll = m['pll']
      //enc = m['enc']
      delete m.pll;
      m.payload = b.slice(5 + lh);
      return m;
    } catch (e) {
      console.log(e);
      throw 'undecodable';
    }
  }

  // accessible for ax-op boxes:
  const send = (ws, d) => {
    // support others
    if (d.enc && d.enc.indexOf('msgpack') > -1) {
      ws.send(to_binary(d));
    } else {
      ws.send(js(d));
    }
  };
  // ----------------------------------------------------------  NR -> Client
  // object cache on NR (for http in req) TODO: more, e.g. tcpsocket
  function setup_object_cache_if_not_done() {
    if (AH.object_cache) return;
    console.log('Creating object cache');
    AH.object_cache = {};
    AH.RED.nodes.eachNode(register_object_removal);
  }

  register_object_removal = (node) => {
    if (node.type === 'http response') {
      const n = AH.RED.nodes.getNode(node.id);
      // node._InputCallbacks is a list with cbs, incl. the normal on input behaviour, all async.
      // ours is just another one:
      n.on('input', pop_msg_from_cache);
      // FIXME : remove this 2nd callback with NR 3.1.1, if he fixed it:
      // https://github.com/node-red/node-red/issues/3815#issuecomment-1796456784
      n.on('input', pop_msg_from_cache);
    }
  };

  function pop_msg_from_cache(msg) {
    const cmsg = AH.object_cache[msg._msgid];
    if (cmsg) {
      console.log('popping', msg._msgid);
      delete AH.object_cache[msg._msgid];
      return cmsg;
    } else {
      // FIXME:see above...
      console.error(
        'message not in cache - Hint: are we on 3.1.1 already and registered delete callback twice for a NR bug workaround?'
      );
    }
  }

  function push_msg_to_cache(msg) {
    // so that we can pull it out later when it comes back from python:
    msg._cached = true;
    AH.object_cache[msg._msgid] = msg;
    console.log('cached:', Object.keys(AH.object_cache).length);
  }
  // client selection:
  function best_client_by_input_node_id(node) {
    // find a suitable client for a function request
    let c;
    let take;
    let os;
    let subj_id;
    let min_open = 1000000;
    const hub = g.AXHub;
    //const axops = g.AXHub.all_ax_ops;

    open_jobs_cur.funcs[node.id] = open = open_jobs_cur.funcs[node.id] || {};

    for (const sck in hub.clients) {
      c = hub.clients[sck];
      subj_id = c.supported_ax_entry_nodes[node.id];
      if (subj_id === undefined) continue;
      open[c.sck] = os = open[c.sck] || 0;
      //console.log('open', os, min_open, open, c.msg.sck)
      if (os < min_open) {
        min_open = os;
        take = c;
        //console.log('taking', open, min_open, c.msg.sck)
      }
    }
    if (take)
      return {
        client: c,
        subject_id: subj_id // In py, all NR inputs get in the stream via subjects
      };

    //        // when its from within a subflow instance than node alias is set and .z will be the subj_id:
    //        subj_id = node._alias ? node.z : node.id
    //        c = 0
    //        for (let sck in hub.clients) {
    //            c = hub.clients[sck]
    //            mapped = c.supported_ax_entry_nodes[node._alias || node.id]
    //            if (mapped == undefined) continue

    //            open[c.sck] = os = open[c.sck] || 0
    //            //console.log('open', os, min_open, open, c.msg.sck)
    //            if (os < min_open) {
    //                min_open = os
    //                take = c
    //                //console.log('taking', open, min_open, c.msg.sck)
    //            }
    //        }
    //        if (take) return {client: take, subject_id: subj_id}
    //        if (c == 0) return
    // no need to dig all the time for clients - but remember that clients come and go and can do different things,
    // so we blacklist not forever:
    console.log('blacklisting (no input node) for 5 sec: ', node.id, node);
    hub.ax_ops_no_send[node.id] = Date.now();
    //FIXME: happens at debug node con into a python pipe:
    //node.error(fn + ': No client found.')
    //node.send('No client')
  }
  function make_py_msg_if_nr_created(msg, chain) {
    if (!msg._ids) {
      const ids = { msg: msg._msgid };
      return {
        type: 'msg',
        func: chain,
        _ids: ids,
        payload: msg.payload,
        ts: Date.now() / 1000
      };
    } else {
      msg.sent = msg.sent ? msg.sent + 1 : 0; // seems info only
      return msg;
    }
  }
  function broadcast_msg_to_clients(msg) {
    /* sending to all connected clients */
    const hub = g.AXHub;
    let c, pymsg;
    const r = {};
    for (const sck in hub.clients) {
      c = hub.clients[sck];
      pymsg = make_py_msg_if_nr_created(msg, 'broadcast');
      pymsg.type = 'broadcast';
      AH.send(c.ws, pymsg);
      r[sck] = true;
    }
    return r;
  }
  function msg_to_client(fn_, msg, node) {
    /*
     * The first ax node (=node param) of a pipeline got a message from a node red operator
     * e.g.: ax-op at input:  g.AXHub.msg_to_client(node.name, msg, node)
     * We find the best suited client process and pass the message downstream.
     */
    // pyop -> NR op
    //      -> pyop2  Are we pyop2 which got .send when we received msg for NR op?
    const blcklst = AH.ax_ops_no_send[node.id];
    if (blcklst && Date.now() - blcklst < 5000) return;
    const chain = fn_.split(/#/, 100); // dont decode for perf here
    const fn = chain[0];
    const c = best_client_by_input_node_id(node);
    if (!c) return;
    // is this created here, or was it from python and should go there again?:
    let pymsg = make_py_msg_if_nr_created(msg, chain);

    //flw is the name of the virtual NR ingress subject in python:
    //if (node.id != this.id)
    pymsg._ids.flw = c.subject_id;
    pymsg._ids.nr_inp_node = node.id;
    //if (msg.enc) pymsg.enc = msg.enc
    open_jobs_cur.funcs[node.id][c.sck] += 1;
    //console.log(open_jobs_cur)
    // when there is a sync client waiting for result we have to know that, so:
    if (must_cache(msg)) {
      push_msg_to_cache(msg);
      pymsg._cached = true;
    }
    AH.send(c.client.ws, pymsg);
    //AH.waiting[msg._msgid] = node
  }
  // TODO: formalize object detection, i.e. the need to cache, msg.req for http is not the only sync proto:
  const must_cache = (msg) => Boolean(msg_is_from_NR_http_in(msg) || false);
  const msg_is_from_NR_http_in = (msg) => Boolean(msg.req?.res?._flushOutput); //only nr has these. py http does have .req

  // ws python program registered with their web sockets in clients dict
  // job clients subscribe on the $jobresult_pub subject
  g.AXHub = AH = {
    send: send,
    clients: {},
    subj_jobres: new Rx.Subject(),
    //on_snk_subscription: on_snk_subscription,
    msg_to_client: msg_to_client,
    broadcast_msg_to_clients: broadcast_msg_to_clients
    //waiting: {},
  };
  rebuild_all_flows(AH, RED, g);
  strmdbg = (txt) =>
    //stream debug
    rx.map((x) => {
      console.log('breaking at', txt, x);
      debugger;
      return x;
    });

  strmlog = (txt) =>
    rx.map((x) => {
      console.log(txt, x);
      return x;
    });

  AH.$jobres = AH.subj_jobres
    .pipe(
      rx.map((client_msg) => {
        /* A message from upstream.
         * At registration, clients did only deliver the entry nodes (client's sources from NR)
         * not the exit nodes.
         * At registration, we stored entry nodes in AH[client].supported_ax_entry_nodes
         * and therefore have a means to check if we need to send down or simply forward msgs
         * like this one.
         * Here we got a message from the client (upstream) and its maybe the first of that
         * node instance.
         * Remember: instance ids are different than configured node ids (subflow unwrapping)
         * => So we look instance id up and cache it for the next ones.
         */
        let idi;
        const msg = client_msg.msg;
        //const client = client_msg.client;

        const id = msg._ids.last_op;
        idi = AH.supported_ax_exit_nodes[id];
        if (!idi) {
          idi = get_node_instance_id(id);
          AH.supported_ax_exit_nodes[id] = idi;
        }
        // .virt.noop inserted after ax-cond in build.py. Its virtual, hub not knows it, so go back, if present:
        // Note: This remove works because client inserted the noop with id according to that convention:
        const node = nodes.getNode(idi.replace('.virt.noop', ''));

        // in py we have that dict for ids, turn it back:
        if (!node) {
          console.log(JSON.stringify(msg));
          console.log('Job result without an operator sending it!!!');
          return;
        }
        msg._msgid = msg._ids.msg;
        if (msg._cached) {
          const cmsg = AH.object_cache[msg._msgid];
          if (cmsg) {
            // will be removed from cache later, at http resp send, via an input callback there:
            msg.req = cmsg.req;
            msg.res = cmsg.res;
          }
        }
        if (node.wires.length > 1) {
          const msgs = [msg];
          for (let j = 1; j < node.wires.length; j++) msgs.push(msg);
          node.send(msgs);
        } else node.send(msg);
      })
    )
    .subscribe((x) => x);
  // function fwd_pymsg_to_js_child_ops(all_ax, axop, msg) {
  //     let ws, id, n
  //     for (var j = 0; j < axop.wires.length; j++) {
  //         ws = axop.wires[j]
  //         for (var k = 0; k < ws.length; k++) {
  //             id = ws[k]
  //             if (!all_ax[id]) {
  //                 n = nodes.getNode(ws[k])
  //                 if (n) {
  //                     n.send(msg)
  //                 }
  //             }
  //         }
  //     }
  // }

  function set_editor_status(node, AH) {
    const count = Object.keys(AH.clients).length;
    if (!count) {
      node.status({
        fill: 'red', //shape: 'dot',
        text: 'No Connections '
      });
    } else {
      node.status({
        text: `Workers: ${count}`
      });
    }
  }
  // Collecting all websocket clients in a stream of streams:
  AH.$$all_msgs = new g.Rx.Subject();

  // messages generated by ourselves (e.g. subs_change)
  AH.$hub_msgs = new g.Rx.Subject();

  function cut_wires_to_py_entry_nodes(cut_wires) {
    let frm;
    let to;
    let nfrom;
    let ws;
    let did;
    let nw;
    for (let p = 0; p < cut_wires.length; p++) {
      frm = cut_wires[p][0];
      ifrm = get_node_instance_id(frm);
      to = cut_wires[p][1];
      ito = get_node_instance_id(to);

      nfrom = nodes.getNode(ifrm);
      for (let k = 0; k < nfrom.wires.length; k++) {
        ws = nfrom.wires[k];
        wg = [];
        for (let j = 0; j < ws.length; j++) {
          did = ws[j];
          if (did === ito) {
            ws.splice(j, 1);
          }
        }
      }
    }
  }

  function get_node_instance_id(ax_id) {
    /* Only the node ids on root, i.e. on the tabs are ident to their instances
     * When we configured subflows, their ids are different, per (nested?) instance
     * Here we dig down the instances tree to find the match between python instance
     * id scheme (pth style, e.g. id_toplevel/id_subflowinstance1/id_sfi2/.../id_operator)
     * and node red's scheme.
     * Note: If we wanted to keep them in sync we would have to send down the whole tree at
     * registration time so they could be used at build reindexing time down at the client.
     * TODO: check projects - if subflow levels get too deep, e.g. > say 5 levels and
     * indexes are default and not shortened (i.e. like e905034a.721ea) we'll end up in
     * *pretty* long instance ids in python, which are transferred for every NR/Py comm event!
     * Then we should try keep them in sync, or simply count up at python indexing time and
     * send an indirection dict up, once at registration, after build.
     */
    let nodemap;
    let dict;
    let _k1;
    let _v1;
    let op;
    const parts = ax_id.split('/');
    if (parts.length === 1) {
      return parts[0];
    }
    const root_node = AH.RED.nodes.getNode(parts[0]);
    // subflow walk: find the instance id of the deeply nested ax node,
    // which node red will see the input event later at data flow time
    nodemap = root_node._flow;

    for (let k = 1; k < parts.length; k++) {
      dict = Object.entries(nodemap.flow.nodes).filter(
        ([_k1, _v1]) => v1._alias === parts[k]
      );
      op = nodemap.activeNodes[dict[0][0]];
      nodemap = op._flow;
    }
    return op.id;
  }

  function register_pipes_by_entry_node_id(client) {
    /*
     * client: The registration message of a new client.
     * We are adding this client to our clients_by_entry_op dict
     * So that at data flow we have a fast lookup for the list of clients which
     * can handle the data.
     */
    let src;
    const p = client.payload;
    let id;
    client.funcs = p.funcs;
    client.pipes = p.pipes;
    client.supported_ax_entry_nodes = {};
    cut_wires_to_py_entry_nodes(p.nr_cut_wires);
    for (let i = 0; i < p.pipes.length; i++) {
      srcs = p.pipes[i].srcs;
      for (let j = 0; j < srcs.length; j++) {
        src = srcs[j];
        id = get_node_instance_id(src);
        client.supported_ax_entry_nodes[id] = src;

        //                 if (AH.all_ax_ops[src]) {
        //                     if (!o[src]) o[src] = []
        //                     // can have this src more often in client's pipes - at splits we
        //                     // get more pipes on the client. We register one client only
        //                     // once per node red entry op reprsentation:
        //                     if (o[src].indexOf(msg) == -1) o[src].push(msg)
        //                 }
      }
    }
  }

  //        for (var i = 0; i < p.pipes.length; i++) {
  //            srcs = p.pipes[i].srcs_physical
  //            for ([src, nfs] of Object.entries(srcs)) {
  //                // if this is not a py op then we='ll never need to send to it:
  //                if (!AH.all_ax_ops[src]) {
  //                    console.warn('Pipe source not ax', src)
  //                    continue
  //                }
  //                if (nfs == src) {
  //                    // non virutal
  //                    o[src] = true
  //                    continue
  //                }
  //                // walk down the instance tree:
  //                let idm,
  //                    sfi = AH.RED.nodes.getNode(nfs.ids[0])._flow
  //                for (var si = 1; si < nfs.ids.length; si++) {
  //                    idm = sfi.node_map[nfs.ids[si]]
  //                    if (idm._alias == src) break
  //                    sfi = sfi.subflowInstanceNodes[idm.id]
  //                }
  //                //if (z != src) src = z + ':' + src
  //                if (!o[src]) o[src] = {}
  //                // can have this src more often in client's pipes - at splits we
  //                // get more pipes on the client. We register one client only
  //                // once per node red entry op reprsentation:
  //                //if (o[src].indexOf(msg) == -1) o[src].push(msg)
  //                first_z = nfs.zs[1]
  //                o[src][first_z] = idm
  //                ///if (o[src].indexOf(z) == -1) o[src].push(z)
  //            }
  //        }

  // functions run, dependeint on type attribute of messages:
  process_msg = (msg_type) => {
    return {
      subs_change: (r) => {
        /*
         * Subscription change.
         * One snk might be for many flows. We do NOT want to send changes down per
         * flow but only for the first flow and rely on client to apply the status
         * change on all its flows with that snk id
         */
        function send_subs_change(msg) {
          /* A snk got a subscription - e.g. a wss connect was seen.
           * Signal that down to the clients so they start subscribing
           */
          let c;
          const job = {
            type: 'subs_change',
            payload: {
              snk: msg.node,
              mode: msg.mode
            },
            ts: Date.now()
          };
          for (const sck in AH.clients) {
            c = AH.clients[sck];
            AH.send(c.ws, job);
          }
        }

        const msg = r.msg;
        const count = msg.connected;
        const snk = AH.dyn_snks[msg.node];
        if (msg.mode === 'subscribed') {
          if (snk === 'subscribed') {
            // client has taken the subscription status from other flow already
            console.log('snk already marked subscribed');
            return;
          } else {
            AH.dyn_snks[msg.node] = 'subscribed';
            send_subs_change(msg);
          }
        } else {
          if (snk === 'subscribed') {
            // we get the callback just *before* a close
            if (count < 1) {
              AH.dyn_snks[msg.node] = 'unsubscribed';
              send_subs_change(msg);
            }
          }
        }
      },
      register: (r) => {
        //TODO: parse the pippeline results and take this client out for the non built ones
        if (!(r && r.msg && r.msg.payload && r.msg.payload.funcs)) return r; //incomplete
        const p = r.msg.payload;
        console.log('register client'); //, JSON.stringify(p, 0, 4))
        setup_object_cache_if_not_done(); //AH)
        r.ws.cln = p.cln; // keep
        register_pipes_by_entry_node_id(r.msg);
        delete r.msg.payload;
        r.msg.sck = r.ws.sck;
        r.msg.ws = r.ws;
        AH.clients[r.ws.sck] = r.msg;
        send(r.ws, {
          type: 'status',
          payload: { registered: r.ws.sck },
          ts: Date.now()
        });
        set_editor_status(node, AH);
        node.warn(`registered client: ${r.ws.cln} [${r.ws.sck}]`);
        //console.log("registered client");
        return r;
      },
      flow_def: (r) => {
        const client_msg = r;
        //const hub = AH;

        //const fn = `${AH.RED.settings.userDir}/client_flows.json`;
        //const p = projects;
        projects
          .getActiveProject({
            user: 'root'
          })
          .then((v) => {
            //TODO: git commit it? We have all git version infos in the promise
            // Or should we compare versions and only accept newer versions?
            // I think not since we restart anyway
            const f = JSON.stringify(client_msg.msg.payload.flows);
            const fn = `${v.path}/flows.json`;
            //const red = hub.RED;
            fs.writeFile(fn, f, (err) => {
              // throws an error, you could also catch it here
              if (err) throw err;

              // success case, the file was saved
              console.warn(
                'Flows from client saved - restarting',
                fn,
                v.package
              );
              // better than process exit
              // chrome debugger tool window has to be killed, unfortunatelly
              throw new Error('restarting');
            });
          });
      },
      status: (r) => {
        console.log('Client status', r.msg);
      },
      msg: (r) => {
        // processing a job *response* from the client
        // set open jobs -1 - this is just for metrics and is reset every sec:
        const open = open_jobs_cur.funcs[r.msg._ids.nr_inp_node];
        if (open) open[r.ws.sck] = (open[r.ws.sck] || 1) - 1;
        // for runtime stats:
        r.msg.dt = Date.now() - r.msg.ts;
        AH.subj_jobres.next({
          msg: r.msg,
          client: r.ws.sck
        });
      },
      closed: (r) => {
        // injected by hub on wsclose, not(!) a message from client
        node.warn(`client closed ${r.ws.cln}`);
        if (AH.clients[r.ws.sck]) delete AH.clients[r.ws.sck];
        set_editor_status(node, AH);
      },
      undefined: (_r) => {
        log('no type');
        //debugger;
      }
    }[msg_type];
  };

  AH.$all_msgs = AH.$$all_msgs
    .pipe(
      rx.mergeAll(),
      rx.groupBy((r) => r.msg.type),
      rx.mergeMap((s) => s.pipe(rx.map(process_msg(s.key))))
    )
    .subscribe((x) => x);

  AH.$$all_msgs.next(AH.$hub_msgs); //.pipe(rx.distinctUntilChanged(compare)))

  //AH.subj_jobres.pipe(rx.bufferTime(1000), rx.map(job_stats)).subscribe(x => x)

  const ax_ws_port = this.server.address().port + 1;
  console.log('Opening ax-hub server, port', ax_ws_port);
  const wss = new ws.Server({
    path: '/ws/ax-hub',
    port: ax_ws_port
  });
  AH.wss = wss;

  wss.on('connection', function connection(ws, _req) {
    /* Hub <-> Clients websocket server
     *
     * See nrclient.py for handshake protocol.
     * Short version:
     * register exchanges infos, client starts.
     * client sends its function in register,
     * nr answers with flows to be built.
     * */
    $msgs = Rx.Observable.create((obs) => {
      ws.on('open', function incoming(_message) {
        console.log('Got open');
      });
      ws.on('close', () => {
        console.log('Got close');
        obs.next({
          msg: {
            type: 'closed'
          },
          ws: ws
        });
        obs.complete();
      });

      ws.on('message', function incoming(message) {
        try {
          m = jp(message);
          console.log('Got msg', message.length);
        } catch (_e) {
          try {
            m = from_binary(message);
            console.log('Got binary msg', message.length);
          } catch (e) {
            console.log(e);
          }
        }
        obs.next({
          msg: m,
          ws: ws
        });
      });
    });

    // auth here
    ws.sck = newid(); // session id.

    // we send down all flows at connect:
    const msg = {
      type: 'register',
      _ids: {
        sck: ws.sck,
        hbn: 'hub1'
      },
      payload: {
        pipelines: AH.all_flows,
        dyn_snk_types: AH.dyn_snk_types,
        dyn_snks: AH.dyn_snks
      }
    };
    //const f = flows;
    send(ws, msg);
    node.log(`new connection: ${ws.sck}`);
    // we want ALL py clients' messages in one global upstream:
    // so we put the new clients messages stream as one item into the global one:
    AH.$$all_msgs.next($msgs);
  });
  console.log('Opened ax server');

  node.log('have ax hub');

  // ----------------------------------------------------------------------   Metrics
  // We do a bit more to have cool "best client" selection decision posssiblitiies
  let open_jobs_cur = {
    funcs: {}
  }; // current open
  const stats_rate = {
    funcs: {}
  };
  const stats_total = {
    by_cln: {}
  };
  AH.stats_rate = stats_rate;
  AH.stats_total = stats_total;

  function stats_reset() {
    for (const key in stats_rate) {
      delete stats_rate[key];
    }
    stats_rate.funcs = {};
  }

  function job_stats(one_sec) {
    //if (one_sec.length == 0) return
    open_jobs_cur = {
      funcs: {}
    };
    stats_reset();
    Rx.from(one_sec)
      .pipe(
        rx.groupBy((r) => `${r.func[0]}::${r.sck}`),
        rx.mergeMap((s) =>
          s.pipe(
            rx.reduce(
              (acc, r, i) => {
                acc.dt += r.dt;
                acc.total += 1;
                return acc;
              },
              {
                dt: 0,
                total: 0
              }
            ),
            rx.map((res) => {
              if (!res.total) return;
              let m;
              const fs = s.key.split('::');
              const func = fs[0];
              const sck = fs[1];
              let cln = AH.clients[sck];
              if (!cln) return;
              cln = cln.cln;
              res.dt = res.dt / res.total;
              stats_rate.funcs[func] = m = stats_rate.funcs[func] || {};
              m[sck] = res;
              // increment total counters:
              const t = stats_total.by_cln;
              t[cln] = t[cln] || {};
              t[cln][func] = m = (t[cln][func] || 0) + res.total;
              console.log(func, cln, res, 'total: ', m);
            })
          )
        )
      )
      .subscribe((x) => x);
  }
}
// -----------------------------------------------------------------------------   Node
module.exports = function (RED) {
  function AXHub(config) {
    /* Run at every redeploy and at start */
    RED.nodes.createNode(this, config);
    const g = this.context().global;
    // node.on('close', function(msg) { function closed() { console.log('Closed websocket') } g.AXHub.wss.close() })
    this.on('input', function (msg) {
      /* Serving Hub's http api */
      console.log('Input to hub');
      const hub = g.AXHub;
      if (msg.req?.url == '/api/v1/broadcast') {
        msg.payload = JSON.parse(msg.payload);
        msg.payload.hub_clients = hub.broadcast_msg_to_clients(msg);
        return this.send(msg);
      }
      if (msg.payload.broadcast) {
        hub.broadcast_msg_to_clients(msg);
        return this.send(msg);
      }
      const url = msg.req.url;
      let fn = url.split('/api/v1/')[1];
      // api call:
      if (fn) {
        if (fn == 'clients') {
          for (let i = 0; i < 10; i++) {
            this.send(msg);
            //return hub.msg_to_client(fn, msg, this);
          }
        }
      }

      const client = url.split('/status/')[1];
      const clients = hub.clients;
      msg.payload = {
        stats: {
          rate: hub.stats_rate,
          total: hub.stats_total
        }
      };
      if (!client) {
        msg.payload.clients = clients;
      } else {
        msg.payload.clients = [];
        g.Rx.from(g._.toPairs(clients))
          .pipe(g.rx.filter((r) => r[1].cln === client))
          .subscribe((r) => msg.payload.clients.push(r[1]));
      }
      this.send(msg);
    });

    //scan_topology(config, g) //find_all_ax_pipelines(config, g)

    if (g.AXHub) {
      console.log('closing all clients of old instance');
      // let them unsubscribe and reconnect to get any new pipelines:
      // TODO: gk verify - is rebuild_all_flows enough or should we NOT return here
      // and keep calling ax_make_hub?
      rebuild_all_flows(AH, RED, g);
      // this for sure:
      g._.toPairs(AH.clients).filter((x) => x[1].ws.close());
      return;
    }
    //console.log('making new hub');
    RED.ax_make_hub(this, g, RED);
  }

  function wait_for_port() {
    // when started with node red.js we don't have express server from the start:
    if (RED.server.address()) {
      console.log('AX-Hub: Have server port:', RED.server.address().port);
      RED.ax_make_hub = ax_make_hub;
      RED.nodes.registerType('ax-hub', AXHub);
      console.log('AX-Hub: Started ax-hub at', RED.server.address().port + 1);
      return;
    }
    return setTimeout(wait_for_port, 0.05);
  }

  console.log('AX-Hub: waiting for server port...');
  wait_for_port();
};

// begin_archive # configured vi to only go here on G

//     compare = (x, y) => {
//         /* on this hub some messages are generated double */

//         return (
//             // new ws client -> all flows with that one as snk will fire:
//             x.msg.type == 'subs_change' &&
//             x.msg.mode == y.msg.mode &&
//             x.msg.id == y.msg.id
//         )
//     }

//@format
//
//
// export const log = (...args) => data => {
//     console.log.apply(null, args.concat([data]))
//     return data
// }

// function scan_topology(hub_config, g) {
//
//     // identifying the interesting stuff for us:
//     let all
//     g.ax_pipelines = {}
//     g.first_nodes = []
//     g.all_ax = []
//     g.snks = []
//     g.ax_link_outs = []
//     g.ax_link_ins = []
//     g.all_nodes = all = hub_config._flow.global.allNodes
//     if (!all) {
//         g.all_nodes = all = hub_config._flow.flow.configs
//         if (!all) {
//             console.log('no nodes here')
//             return
//         }
//     }

//     let n, ids
//     let wires = []
//     let l = Object.entries(all)

//     console.log('Scanning topology. Nodes:', l.length)

//     for (var i = 0; i < l.length; i++) {
//         n = l[i][1]
//         if (!is_ax(n) || n.type == 'ax-hub') continue
//         g.all_ax.push(n)
//         if (n.type == 'ax-link out') g.ax_link_outs.push(n)
//         if (n.type == 'ax-link in') g.ax_link_ins.push(n)

//         for (var j = 0; j < n.wires.length; j++) {
//             for (var k = 0; k < n.wires[j].length; k++) {
//                 wires.push(n.wires[j][k])
//             }
//         }
//     }
//     for (var i = 0; i < g.all_ax.length; i++) {
//         n = g.all_ax[i]
//         if (wires.indexOf(n.id) == -1) g.first_nodes.push(n)
//     }
// }

// function find_snks(n, snks, all) {
//     /*
//      * While building the ax_pipelines, from all ax-start nodes,
//      * this goes INTO the tree from all pipeline endings (non ax) nodes,
//      * returns all flow ends
//      * Also a pipeline may end with an ax-snk
//      *
//      * */
//     if (!n.id) console.log('ERROR: snk is none!')
//     // console.log(n, '????????????????????????????????????')
//     // if (n.id == 'ax-op-2') {
//     //     debugger
//     // }
//     console.log('find_snk', n.id)
//     let w
//     let i, j, cn
//     if (n.links != null && n.type.indexOf('out') > -1) {
//         if (!n.links.length) {
//             snks[n.id] = n
//             return
//         }
//         for (let i = 0; i < n.links.length; i++) {
//             find_snks(all[n.links[i]], snks, all)
//         }
//         return
//     } else {
//         if (!n.wires || !n.wires.length) {
//             snks[n.id] = n
//             return
//         }
//     }

//     for (let i = 0; i < n.wires.length; i++) {
//         w = n.wires[i]
//         for (let j = 0; j < w.length; j++) {
//             cn = all[w[j]]
//             find_snks(cn, snks, all)
//         }
//     }
// }

// function mark_always_subscribed_snks(hub, RED, g) {
//     /* We identify ALL ax nodes and find out if they connect to ONLY permanent snks
//      * This enables the feature to signal subs_change down, producing only on demand
//      */
//     const scanned_ids = {}
//     let n
//     function find_non_permanent_snks(id) {
//         let have, my_dyn_snks, nwid, nw
//         have = scanned_ids[id]
//         // already scanned (comming after the scanning one)
//         if (have) return have
//         scanned_ids[id] = my_dyn_snks = []
//         n = hub.by_id[id]
//         console.log('find dyn snks', n)
//         for (var i = 0; i < n.wires.length; i++) {
//             ws = n.wires[i]
//             for (var j = 0; j < ws.length; j++) {
//                 nwid = ws[j]
//                 nw = hub.by_id[nwid]
//                 if (nw.wires.length == 0) {
//                     if (on_sub_change_by_dyn_snk_type[nw.type]) {
//                         my_dyn_snks.push(nwid)
//                     }
//                 } else {
//                     my_dyn_snks.push(...find_non_permanent_snks(nwid))
//                 }
//             }
//         }
//         return my_dyn_snks
//     }
//     all_dyn_subs = {}
//     for (const [id, node] of Object.entries(hub.all_ax_ops)) {
//         dyn_snks = find_non_permanent_snks(id)
//         for (var i = 0; i < dyn_snks.length; i++) {
//             n = hub.by_id[dyn_snks[i]]
//             on_sub_change_by_dyn_snk_type[n.type](hub, RED, g, n, node)
//         }
//     }
// }

//function find_all_ax_pipelines(hub_config, g) {
//    /*
//     * Exchanged downstream at handshake (register) time.
//     *
//     * Currently we do NOT tell the python client about all our pipelines, just send
//     * down the specific ones for him, with ax-... nodes:
//     * TODO: Is this smart? Or should python know about ALL wirings
//     * (violating the main principle of event driven architectures) ?
//     */
//    console.log('building ax_pipelines', g.ax_pipelines)

//    function set_props(m, keys, n) {
//        for (var i = 0; i < keys.length; i++) {
//            k = keys[i]
//            m[k] = n[k]
//        }
//    }

//    function recurse_build(id, flow, all) {
//        let w,
//            sub,
//            subs,
//            n = all[id]

//        if (!is_ax(n)) {
//            console.log('find snks for', n.id)
//            find_snks(n, flow.snks, all)
//            return
//        }
//        if (n['type'] == 'ax-snk') {
//            flow.snks[n.id] = n
//        }
//        let k,
//            m = {}
//        let keys = Object.getOwnPropertyNames(n)
//        set_props(m, keys, n)
//        flow.flow.push(m)
//        w = n.wires
//        if (w.length == 0) {
//            return
//        } else if (w.length == 1) {
//            recurse_build(w[0][0], flow, all)
//        } else {
//            sub_flows = []
//            flow.flow.push(sub_flows)
//            for (var i = 0; i < w.length; i++) {
//                sub_flow = []
//                recurse_build(w[i][0], {snks: flow.snks, flow: sub_flow}, all)
//                sub_flows.push(sub_flow)
//            }
//        }
//    }
//    function build_ax_flow(node, all, g) {
//        var l
//        g.ax_pipelines[node.id] = flow = {snks: {}, flow: []}
//        recurse_build(node.id, flow, all)
//        //console.log(JSON.stringify(g.ax_pipelines, 0, 4))
//    }

//    let firsts = g.first_nodes
//    for (var i = 0; i < firsts.length; i++) {
//        build_ax_flow(firsts[i], g.all_nodes, g)
//    }
//    console.log('pipelines built:', Object.keys(g.ax_pipelines).length)
//}

//@format
//
module.exports = function(RED) {
    function AXSink(config) {
        RED.nodes.createNode(this, config)
        var node = this
        node.on('input', function(msg) {
            let g = node.context().global
            g.AXHub.msg_to_client(node.name, msg, node)
        })

        //            // we run in python, not here. This WAS run in python:
        //            // if (msg.ax_complete) {
        //            //     node.send(msg)
        //            //     return
        //            // }
        //            //console.log(node.name + ' input', JSON.stringify(msg))
        //            if (!node.name) {
        //                let wmsg = 'ax-op node needs name (python function name)'
        //                node.warn(wmsg)
        //                return
        //            }
        //            let r = RED
        //            let g = node.context().global
        //            // this message may be from a JS node:
        //            console.log('----------------------------------------------------')
        //            console.log('Got snk msg', msg)
        //            g.AXHub.msg_to_client(node.name, msg, node)
        //        })

        //node.on('input', function(msg) {
        //    // we run in python, not here. This WAS run in python:
        //    if (msg.ax_complete) {
        //        node.send(msg)
        //        return
        //    }
        //    if (!node.name) {
        //        let wmsg = 'ax-snk node needs name (python function name)'
        //        node.warn(wmsg)
        //        return
        //    }
        //    let r = RED
        //    let g = node.context().global
        //    console.log('ax-snk received js input!?', msg)
        //    node.error('ax-snk received js input!?')
        //    //g.AXHub.run(node.name, msg, node)
        //})
    }
    RED.nodes.registerType('ax-snk', AXSink)
}

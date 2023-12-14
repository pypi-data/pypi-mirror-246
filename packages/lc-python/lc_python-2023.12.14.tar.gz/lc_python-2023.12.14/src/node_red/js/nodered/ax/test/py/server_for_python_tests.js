//@format

/*
 * Dynamic loading of test specs, for the python node_red module tests:
 *
 */
process.title = 'server_for_python_tests'
console.log(process.env)
var NRH = process.env.NODE_RED_HOME
const d_nr = NRH + '/../@node-red'
//const d_nr = 'node_modules/@node-red'
const d_core = d_nr + '/nodes/core'
const fn_test_file = '/tmp/node_red_tests.json'
var should = require('should')
var fs = require('fs')
var helper = require('node-red-node-test-helper')
var hubNode = require('../../ax-hub.js')
var opNode = require('../../ax-op.js')
var srcNode = require('../../ax-src.js')
var snkNode = require('../../ax-snk.js')
var condNode = require('../../ax-cond.js')
var joinNode = require('../../ax-join/ax-join.js')
//var ws = require("ws");
//var when = require("when");
//var should = require("should");
//var helper = require("node-red-node-test-helper");
//
var websocketNode = require(d_core + '/network/22-websocket.js')
var fileNode = require(d_core + '/storage/10-file.js')
var httpInNode = require(d_core + '/network/21-httpin.js')
var debugNode = require(d_core + '/common/21-debug.js')
var injectNode = require(d_core + '/common/20-inject.js')
var linkNode = require(d_core + '/common/60-link.js')
var functionNode = require(d_core + '/function/10-function.js')
const {spawn} = require('child_process')

// monkeypatch/intercept the node red log:
var Log = require(d_nr + '/util').log
Log.log = msg => {
    // Fatal: 10, Error: 20, Warn: 30, Info 40, then ridiculous
    if (msg.level > 40) return
    // ignoring this one, occurs but no problem
    if (msg.level == 20 && msg.id == 'ws.out.dflt') return
    if (msg.level < 30) console.log('!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    console.log('NR Log capture:', msg)
    if (msg.level < 30) console.log('!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
}

var _ = require('lodash')
var zlib = require('zlib')
var ws = require('ws')
var os = require('os')
var Rx = require('rxjs')
var rx = require('rxjs/operators')
var rx = require('rxjs/operators')
var mlog = require('mocha-logger')
function us() {
    return {
        functionGlobalContext: {
            _: _,
            ws: ws,
            os: os,
            Rx: Rx,
            rx: rx,
            zlib: zlib,
        },
    }
}
helper.init(require.resolve('node-red'))
// currying the log function, to include always the test nr:
const get_log = nr => {
    const _log = (...args) => (...data) => {
        mlog.log.apply(null, args.concat([data]))
        return data
    }
    return _log(nr)
}

//
const err = mlog.error
helper.Rx = Rx
helper.rx = rx
helper.count = 1
helper.test_flow = null

// CAUTION: Leave the first two nodes at position 0 and 1 !!!!
// We'll wire the test flows against them, while testing:
// {
//     id: 'debug',
//     type: 'debug',
//     z: 'tests',
//     name: '',
//     wires: [],
// },
// {
//     id: 'httpin',
//     type: 'http in',
//     z: 'tests',
//     name: '',
//     url: '/tests/http_post',
//     method: 'post',
//     upload: false,
//     wires: [['allin']],
// },
// {
//     id: 'httpout',
//     type: 'http response',
//     z: 'tests',
//     name: '',
//     statusCode: '',
//     headers: {},
//     wires: [],
// },

helper.init_flow = [
    {
        id: 'allin',
        type: 'function',
        z: 'tests',
        name: '',
        // split between test control to us (input hook on wsout.dflt) and test paylod:
        // after reconfigure with real test pipeline, the debug node will be the test pipeline entry point:
        func: 'return msg.reconfigure ? [msg, null] : [null, msg]',
        outputs: 2,
        noerr: 0,
        wires: [['ws.out.dflt'], []],
    },
    {
        id: 'tests',
        type: 'tab',
        label: 'Flow 1',
        disabled: false,
        info: '',
    },
    {
        id: 'ws.srv',
        type: 'websocket-listener',
        z: 'tests',
        path: '/ws/tests/dflt',
        wholemsg: 'true',
    },
    {
        id: 'wsin',
        type: 'websocket in',
        z: 'tests',
        name: '',
        server: 'ws.srv',
        client: '',
        wires: [['debug', 'allin']],
    },
    {
        id: 'ws.out.dflt',
        type: 'websocket out',
        z: 'tests',
        name: '',
        server: 'ws.srv',
        client: '',
        wires: [],
    },
]

// ---------------------------------------------------------------- end setup
function testflow(done) {
    helper.test_count += 1
    var info = get_log(helper.test_count)
    info('Test flow start')
    var nod,
        n,
        flw = helper.test_flow || JSON.parse(JSON.stringify(helper.init_flow))

    info('Got flow', JSON.stringify(flw, null, 4))
    //'for copy and paste
    info(JSON.stringify(flw))
    helper.load(
        [
            hubNode,
            websocketNode,
            functionNode,
            debugNode,
            injectNode,
            linkNode,
            opNode,
            srcNode,
            snkNode,
            condNode,
            joinNode,
            fileNode,
        ],
        flw,
        function () {
            //hub.should.have.property('name', 'ax-hub')
            var wsout = helper.getNode('ws.out.dflt')
            wsout.should.have.property('id', 'ws.out.dflt')
            var hub = helper.getNode('ax-hub')
            console.log('hub', hub)
            // var allin = helper.getNode('allin')
            // allin.should.have.property('id', 'allin')
            // var debug = helper.getNode('debug')
            var job, jn
            wsin.on('input', function (msg) {
                var i = 23
                debugger
            })
            wsout.on('input', function (msg) {
                // unfortunatelly we can not return anything on this test websocket
                // -> the test client does not get on_message invoked for output,
                // this is only to reconfigure node red
                // Checking by the test client in test_node_red is done by listenting
                // on the send to NR subject
                info('Testserver got message: ' + JSON.stringify(msg))
                if (msg.payload == 'exit') {
                    debugger
                }
                if (msg.reconfigure) {
                    info('reconfiguring myself for new test flow', msg.reconfigure)
                    helper.test_flow = msg.reconfigure
                    done()
                } // this.send is a noop by the test framework
            })
        },
    )
}
helper.test_count = 0
describe('test flow', function () {
    Rx = helper.Rx
    rx = helper.rx

    beforeEach(function (done) {
        helper.s = {} // local test state
        helper.settings(us())
        helper.startServer(done)
    })

    afterEach(function (done) {
        helper.unload()
        helper.stopServer(done)
    })
    for (var count = 0; count < 1000; count++) {
        it('test ' + count, testflow)
    }
})

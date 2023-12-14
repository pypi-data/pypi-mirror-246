//@format
var should = require('should')
var helper = require('node-red-node-test-helper')
var hubNode = require('../ax-hub.js')
var mapNode = require('../ax-op.js')
var condNode = require('../ax-cond.js')
const {spawn} = require('child_process')
var _ = require('lodash')
var tr069sessions = {}
var zlib = require('zlib')
var ws = require('ws')
var os = require('os')
var Rx = require('rxjs')
var rx = require('rxjs/operators')
var rx = require('rxjs/operators')
var mlog = require('mocha-logger')
var axclients = {}
var axfuncs = {}
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

const info = mlog.log
const err = mlog.error

const here = '/root/.node-red/ax/test'
const simple_client = here + '/py/simple.py'
const fin = {id: 'fin', type: 'helper', z: 'f1'} // the final node, to check the stuff out of us
function _end(done) {
    this.unload()
    this.s = {} // any test helper state from us
    this.settings(us()) // the global settings for hub - must be reset always :-/
    done()
}
helper.end = _end
// ---------------------------------------------------------------- end setup
describe('ax-hub Node', function() {
    before(function(done) {
        helper.s = {} // local test state
        helper.settings(us())
        helper.startServer(done)
    })

    after(function(done) {
        helper.unload().then(() => helper.stopServer(done))
    })

    // afterEach(function(done) {
    //     helper.unload()
    // })

    it('should be loaded', function(done) {
        var flow = [{id: 'hub', type: 'ax-hub', name: 'ax-hub'}]
        helper.load(hubNode, flow, function() {
            var hub = helper.getNode('hub')
            debugger
            hub.should.have.property('name', 'ax-hub')
            helper.end(done)
        })
    })

    it('sync pipeline must work', function(done) {
        var flow = [
            {id: 'f1', type: 'tab', label: 'Test flow'},
            {
                id: 'sum',
                type: 'ax-op',
                z: 'f1',
                name: 'math:sum',
                wires: [['cond']],
            },
            {
                id: 'cond',
                type: 'ax-cond',
                z: 'f1',
                name: '',
                condition: '["payload.sum", ">", 10]',
                wires: [['mult']],
            },
            {
                id: 'mult',
                type: 'ax-op',
                z: 'f1',
                name: 'math:mult',
                wires: [['fin']],
            },
            fin,
            {
                id: 'hub',
                type: 'ax-hub',
                z: 'f1',
                name: 'ax-hub',
                wires: [[]],
            },
        ]

        helper.load([mapNode, condNode, hubNode], flow, function() {
            clients = hub => hub.context().global.AXHub.clients

            var hub = helper.getNode('hub')
            hub.should.have.property('name', 'ax-hub')

            helper.getNode('fin').on('input', function(msg) {
                var p = msg.payload
                info('have fin result', msg)
                // assert the condition, nothing else may pass, plus the pipeline passage:
                if (p.sum > 10 && p.a + p.b == p.sum && p.mult == p.a * p.b) {
                    if (helper.s.is_done) {
                        mlog.success('Tests passed.')
                        process.exit(0)
                    }
                    return // passed
                }
                return done(new Error('assertion failed'))
            })
            function inject() {
                helper.getNode('sum').receive({payload: {a: 1, b: 1}})
                helper.getNode('sum').receive({payload: {a: 0, b: 100}})
                helper.s.is_done = true
                helper.getNode('sum').receive({payload: {a: 10, b: 1}})
            }
            function wait_registered() {
                mlog.pending('waiting for client registration')
                var cs = clients(hub)
                for (var c in cs) {
                    if (cs[c].funcs['math:mult']) {
                        mlog.success('have registered client')
                        return inject()
                    }
                }
                mlog.pending(
                    'Note: This test depends on tests/py/simple_client.py started! ',
                )
                return setTimeout(wait_registered, 1000)
            }
            wait_registered()
        })
    })
})

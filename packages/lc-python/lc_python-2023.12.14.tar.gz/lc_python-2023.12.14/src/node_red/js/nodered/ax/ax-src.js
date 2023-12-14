//@format
//
module.exports = function(RED) {
    function AXSrc(config) {
        RED.nodes.createNode(this, config)
        var node = this
        node.on('input', function(msg) {
            // we run in python, not here. This WAS run in python:
            if (msg.ax_complete) {
                node.send(msg)
                return
            }
            if (!node.name) {
                let wmsg = 'ax-src node needs name (python function name)'
                node.warn(wmsg)
                return
            }
            let r = RED
            let g = node.context().global
            console.log('ax-src received input!?', msg)
            node.error('ax-src received input!?')
            //g.AXHub.run(node.name, msg, node)
        })
    }
    RED.nodes.registerType('ax-src', AXSrc)
}

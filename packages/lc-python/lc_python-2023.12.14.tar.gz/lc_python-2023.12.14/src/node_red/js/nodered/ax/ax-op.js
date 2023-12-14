//@format
//
module.exports = function(RED) {
    function AXOp(config) {
        if (typeof config.kw == typeof '') config.kw = JSON.parse(config.kw)
        RED.nodes.createNode(this, config)
        var node = this
        node.on('input', function(msg) {
            if (!node.name) {
                let wmsg = 'ax-op node needs name (python function name)'
                node.warn(wmsg)
                return
            }
            let g = node.context().global
            g.AXHub.msg_to_client(node.name, msg, node)
        })
    }
    RED.nodes.registerType('ax-op', AXOp)
}

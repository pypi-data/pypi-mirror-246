//@format
//
module.exports = function(RED) {
    function AXCond(config) {
        RED.nodes.createNode(this, config)
        var node = this
        node.condition = node.name || config.condition
        node.on('input', function(msg) {
            let g = node.context().global
            g.AXHub.msg_to_client(node.name, msg, node)
        })
    }
    RED.nodes.registerType('ax-cond', AXCond)
}

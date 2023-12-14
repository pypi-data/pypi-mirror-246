//@format
//
module.exports = function(RED) {
    function AXJoin(config) {
        
        RED.nodes.createNode(this, config)
        var node = this
        node.on('input', function(msg) {
            let g = node.context().global
            g.AXHub.msg_to_client(node.name || 'ax-join', msg, node)
        })
    }
    RED.nodes.registerType('ax-join', AXJoin)
}

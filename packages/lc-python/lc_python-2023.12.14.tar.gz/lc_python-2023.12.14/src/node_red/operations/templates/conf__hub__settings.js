const os = require('os');
var ax_product = process.env.ax_product || 'Axiros';
var ax_title =
    ax_product + ' - Data Flow Editor [Node RED@' + os.hostname() + ']';
module.exports = {
    flowFile: 'flows.json',
    flowFilePretty: true,
    //%(admin_auth||)s,
    uiPort: process.env.PORT || 1880,
    httpStatic: process.env.PROJECT_ROOT + '/data/node-red-static/',
    logging: {
        console: {
            level: '%(log_level||trace)s',
            metrics: true,
            audit: false,
        },
    },
    exportGlobalContextKeys: true,
    externalModules: {},
    editorTheme: {
        header: { title: ax_title },
        //    aurora cobalt2 dark dracula espresso-libre midnight-red monoindustrial monokaioceanic-next oled solarized-dark solarized-light tokyo-night zenburn
        theme: '%(theme||aurora)s',
        page: { title: ax_title },
        palette: {},
        projects: {
            enabled: true,
            workflow: {
                mode: 'manual',
            },
        },
        codeEditor: {
            lib: 'monaco',
            options: {},
        },
    },
    functionExternalModules: true,
    functionGlobalContext: {
        _: require('lodash'),
        tr069sessions: {},
        zlib: require('zlib'),
        ws: require('ws'),
        os: require('os'),
        Rx: require('rxjs'),
        rx: require('rxjs/operators'),
        axclients: {},
        axfuncs: {},
    },
    debugMaxLength: 1000,
    mqttReconnectTime: 15000,
    serialReconnectTime: 15000,
};

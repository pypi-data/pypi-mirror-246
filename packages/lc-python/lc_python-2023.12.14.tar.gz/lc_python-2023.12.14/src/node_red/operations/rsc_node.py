"""
Provides our customized Node-RED

- npm install of all node modules
- style adapations
- starter files bin/hub, bin/hubdebug

To understand which function is run when, check the resources.py
"""

from devapp.app import app, do, system
from devapp.tools import (
    dir_of,
    envget,
    project,
    read_file,
    write_file,
    offset_port,
    exists,
)
import os
import json
import time

j = os.path.join


def set_ax_style(dest):
    app.info('Styling Node-RED')
    here = os.getcwd()
    import devapp as d

    rpl = os.path.dirname(d.__file__) + '/third/rpl'

    def r(*ft, dest=dest):
        for k in ('node-red',):  #'@node-red':
            os.chdir(dest + '/node_modules/' + k)
            app.info('replacing', colors=ft, dir=k)
            cmd = rpl + ' -qiR "%s" "%s" .' % ft
            err = os.system(cmd)
            if err:
                app.die('Could not color replace', cmd=cmd)

    r('8c101c', '8bd124')  # deploy button
    # r('8f0000', '8bd124')  # deploy button
    r('AD1625', '89bd12')  # done button
    r('6e0a1e', '6bb104')  # hover button (done)
    os.chdir(here)

    def mvf(src, t, d_nr=dest):
        d_nr += '/node_modules/@node-red/editor-client/public'
        t = d_nr + '/' + t
        app.info('img', src=src, dest=t)
        os.unlink(t) if exists(t) else 0
        os.system(f'cp "{src}" "{t}"')

    dt = dir_of(__file__) + '/templates'
    mvf(dest + '/ax/icons/ax_fit.svg', 'red/images/node-red.svg')
    mvf(dt + '/node-red-256.svg', 'red/images/node-red-256.svg')
    mvf(dt + '/favicon.ico', 'favicon.ico')


def project_name():
    return project.root().rsplit('/', 1)[-1]


def nr_user_dir():
    dn = os.path.dirname
    d = dn(dn(__file__)) + '/js/nodered'
    return d


def nr_project_dir():
    return nr_user_dir() + '/projects/' + project_name()


def config():
    n = project_name()
    return {
        'fn': 'conf/hub/config.projects.json',
        'content': {'activeProject': n, 'projects': {n: {'credentialSecret': False}}},
    }


default_flow = [
    {
        'id': 'first_tab',
        'type': 'tab',
        'label': 'Flow 1',
    },
    {
        'id': 'axhub.%s' % int(time.time()),
        'type': 'ax-hub',
        'z': 'first_tab',
        'name': 'AX-Hub',
        'x': 100,
        'y': 100,
        'wires': [[]],
    },
]


def flows(api):
    c = api.constant('fn_flows', '')
    if c:
        if not exists(c):
            app.die('Default flows.json file not found', expected=c)
        app.info('Copying default flows.json', flowfile=c)
        f = json.loads(read_file(c))
    else:
        f = default_flow
    return {'fn': 'conf/hub/flows.json', 'content': f, 'keep_existing': True}


def package():
    return {
        'fn': 'conf/hub/package.json',
        'content': {
            'name': project_name(),
            'description': project_name(),
            'version': '0.0.1',
            'dependencies': {},
            'node-red': {
                'settings': {
                    'flowFile': 'flows.json',
                    'credentialsFile': 'flows_cred.json',
                }
            },
        },
    }


def settings(d_node=None):
    # when d_node is passed we try render the settings (requireing node)
    class Settings:
        d_node = None

        def parse_admin_auth(_, v):
            v = v or LB + '}'  # darn TreeSitter
            if v[0] in {LB, LSB}:
                return json.loads(v)

            # admin_users=myadmin:mypass:*,myuser:mypass2:read,...
            def parse_user(u, d_node=_.d_node):
                u, pw, p = [i.strip() for i in (u + ':*').split(':')[:3]]
                cmd = "console.log(require('bcryptjs').hashSync(process.argv[1], 8));"
                node = f'{d_node}/node'
                cmd = f'cd "{nr_user_dir()}" && "{node}" -e "{cmd}" "{pw}"'
                pws = os.popen(cmd).read().strip()
                return {'username': u, 'password': pws, 'permissions': p}

            us = [parse_user(i.strip()) for i in v.split(',')]
            return us

        def __getitem__(self, k, prefix='hub'):
            k, dflt = [i.strip() for i in k.rsplit('||')]
            v = envget(f'{prefix}_{k}', dflt)
            if k == 'admin_auth':
                try:
                    v = self.parse_admin_auth(v)
                    if not v:
                        return ''
                    if isinstance(v, list):
                        v = {'type': 'credentials', 'users': v}
                    return '\nadminAuth:    ' + json.dumps(v, indent=4)
                except Exception as ex:
                    app.die('cannot parse admin auth', v=v, exc=ex)
            return v

    r = {'fn': 'conf/hub/settings.js', 'content': '', 'type': 'js'}
    if d_node:
        t = read_file(dir_of(__file__) + '/templates/conf__hub__settings.js')
        s = Settings()
        s.d_node = d_node
        r['content'] = t % s
    return r


def ax_npm_install_and_link_project(rsc, install=False, verify=False, npm_inst=[0], **kw):
    """This is the *post* action for hub"""
    d = nr_user_dir()
    dp = nr_project_dir()
    if verify:
        from devapp.app import FLG

        if FLG.force_reinstall:
            rsc.post_inst_verify = False
            return

        # if not exists(project.root() + '/flows.json'):
        #     return app.warn('No flows.json')
        # if not exists(dp):
        #     return app.warn('Project not yet linked', dir=dp)
        fn = d + '/package-lock.json'
        s = read_file(fn, dflt='')
        if 'node-red-contrib-axiros' in s:
            npm_inst[0] = True
            return app.info('nr postinstalled - contrib-axiros present in package-lock')
            # return 'node-red-contrib-axiros present in package-lock'
        else:
            rsc.post_inst_verify = False
            return app.warn('NodeRed not installed', missing=fn)
    # install is true here

    # copy_default_files(dest=d)
    d_cnf = project.root() + '/conf/hub'
    npm = d_node = kw['api'].rsc_path(rsc)
    cmd = 'export PATH="%s:$PATH"; cd "%s" && "%s/npm" install ' % (npm, d, npm)
    if not npm_inst[0]:
        do(system, cmd)
    set_ax_style(dest=d)
    os.makedirs(nr_user_dir() + '/projects/', exist_ok=True)
    os.makedirs(d_cnf, exist_ok=True)
    write_file(d_cnf + '/README.md', 'Linked from\n\n%s\n' % dp)

    def link():
        return do(system, 'ln -s "%s" "%s"' % (d_cnf, dp), ll=30)

    if exists(dp):
        if os.path.islink(dp):
            if os.readlink(dp) == d_cnf:
                app.info('Project linked already')
            else:
                app.info('Unlinking old project dir')
                os.unlink(dp)
                link()
        else:
            app.warn('Present but no link (copied?)', project_nr_path=dp)
            app.info('Leaving unchanged', project_nr_path=dp)
    else:
        link()
    api = kw['api']
    p = project.root()
    for m in config(), package(), flows(api), settings(d_node):
        fn = p + '/' + m['fn']

        c = m['content']
        if m.get('type', 'json') == 'json':
            c = json.dumps(c, indent=4)

        if exists(fn):
            if read_file(fn) == c:
                app.info(m['fn'], status='unchanged')
                continue
            else:
                app.warn(
                    m['fn'],
                    status='changed',
                    usr_hint='Remove before deploy to reset to default',
                )
                continue
                # app.warn(m['fn'], status='changed - overwriting')
        else:
            app.info(m['fn'], status='creating')
        write_file(fn, c, mkdir=True)


# ------------------------------------------------------------------- provided
def title(api):
    return api.constant('hub_title', 'AX-Hub')


def hub(dbg=False, **kw):
    d = nr_user_dir()

    p, fn_config = project.root(), config()['fn']
    fn_settings = settings()['fn']

    ls = ' \\\n  '
    pname = project.root().rsplit('/', 1)[-1]
    hub = (
        'node'
        + ls
        + '  node_modules/node-red/red.js --settings "settings.js" --title "%s" --port %s -u .'
    )
    hub = hub % (title(kw['api']), offset_port(1880))
    cmd = kw['cmd'].replace('hub', hub).replace(' --', ls + '  --')
    pe = [
        'cd "%s"' % d,
        'cp "%s/%s" "%s"' % (p, fn_config, '.config.projects.json'),
        'cp "%s/%s" "%s"' % (p, fn_settings, 'settings.js'),
        '',
        '',
        '# Title of UI:',
        'export ax_product="%s"' % title(kw['api']),
        '',
    ]
    return {'cmd': cmd, 'pre_exec': pe}

    # S = nr_user_dir() + '/settings.js'
    # os.unlink(S) if exists(S) else 0
    # app.info('linking', src=fn, tgt=S)
    # os.symlink(fn, S)


def hubdebug(**kw):
    kw['cmd'] = 'hub'
    s = hub(dbg=True, **kw)
    s['cmd'] = 'node --inspect-brk=1882 ' + s['cmd'].split(' ', 1)[1]
    return s


def npm(cmd, rsc, pth, **kw):
    return ':cd "%s" && npm ' % nr_user_dir()


class node:
    # just a namespace for the provides list for hub in the resources file:
    npm = npm
    hub = hub
    hubdebug = hubdebug
    ax_npm_install_and_link_project = ax_npm_install_and_link_project


LB = '{'
LSB = '['

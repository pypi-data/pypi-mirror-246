"""
Boostrapping a new client

Required: Only python and bash

- Creates a bootstrapp venv with required tools 
"""
import datetime
import json
import os, sys
import shutil
import venv

today = datetime.datetime.now().date().strftime('%Y.%m.%d')
try:
    _D_CONDA_ROOT = os.environ['HOME'] + '/lc_client_root'
except:
    pass


class C:
    """config"""

    version = today
    min_ver = '2020.01.01'
    d_conda_root = _D_CONDA_ROOT
    conda_ver = 'latest'
    conda_url = 'https://repo.continuum.io/miniconda/Miniconda3-%s-Linux-x86_64.sh'


# fmt:off
pth                   = lambda fn: os.path.abspath(fn)
dir_of                = lambda fn: os.path.dirname(pth(fn))
cfg_dict              = lambda: {k: getattr(C, k) for k in dir(C) if not k[0] == '_'}
read_existing_config  = lambda: json.loads(read_file(fn_config, dflt='{}'))
have                  = lambda cmd: not os.system(cmd)
run                   = lambda cmd, err=None: True if have(cmd) else die(err or cmd)
run_c                 = lambda cmd, err=None: run(d_conda_root_bin + cmd, err)
die                   = lambda msg: print(msg) and sys.exit(1)

exists                = os.path.exists
fn_config             = C.d_conda_root + '/.lc-config.json'
fn_conda_inst         = dir_of(C.d_conda_root) + '/.miniconda_installer_%s.sh' % C.conda_ver
d_conda_root_bin      = C.d_conda_root + '/bin/'
# fmt:on


def do(f, *a, **kw):
    print(f.__name__)
    return f(*a, **kw)


def read_file(fn, dflt=''):
    if not exists(fn):
        return dflt
    with open(fn) as fd:
        return fd.read()


def rm_root_venv():
    dir_path = C.d_conda_root
    if not exists(dir_path):
        return
    if not input('delete %s?' % dir_path) in 'y':
        die('unconfirmed')
    shutil.rmtree(dir_path)


def download(url, to):
    uto = url, to
    cmd = 'err'
    os.makedirs(dir_of(to), exist_ok=True)
    if have('wget -V'):
        cmd = 'wget "%s" -O "%s"' % uto
    elif have('curl -V'):
        cmd = 'curl "%s" > "%s"' % uto
    run(cmd, err='could not download %s %s' % uto)


def download_conda_installer():
    if exists(fn_conda_inst):
        return
    url = C.conda_url % C.conda_ver
    download(url, to=fn_conda_inst)
    run('chmod +x "%s"' % fn_conda_inst)


def mk_root_venv():
    if exists(d_conda_root_bin):
        return
    os.makedirs(dir_of(C.d_conda_root), exist_ok=True)
    download_conda_installer()
    run(fn_conda_inst + ' -b -p "%s"' % C.d_conda_root)
    run_c('pip install poetry requests')


def write_cfg():
    with open(fn_config, 'w') as fd:
        fd.write(json.dumps(cfg_dict()))


def main():
    cfg = read_existing_config()
    if cfg.get('version', '2000.01.01') < C.min_ver:
        rm_root_venv()
        mk_root_venv()

    do(write_cfg)
    print('done')


if __name__ == '__main__':
    main()

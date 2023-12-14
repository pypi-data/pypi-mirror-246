#!/usr/bin/env python
"""
A client for Node Red - as plugin of the app script.

This is the default way to start a worker and is called from bin/client
"""

"""
Dev:
This module is being imported by product overwrites

Example: in 4A's src/ax4A/plugins/app_ax4A/client.py:

        from operators.plugins.app_operators import client


This modules purpose is to provide the flags of

1. nrclient
2. conf/functions (if present, i.e. when we are in project mode)

both as top level flags then.



"""
import sys
from devapp.app import run_app
from devapp.tools import skip_flag_defines, FLG, project, exists

# must come before the import, to prevent it defining the flags which we steal here:
skip_flag_defines.append('node_red.nrclient')  # noqa: E402
from node_red import nrclient as red  # isort:skip

try:
    # conf/functions.py:
    import functions
except Exception as ex:
    print('Could not import conf/functions.py', str(ex), file=sys.stderr)
    functions = None


class Flags(red.flags, getattr(functions, 'Flags', object)):
    autoshort = ''


# which functions is given via -cf in the client wrapper, which we leave as config file:
# i.e. we do *not* hard provide the functions tree at functions.Functions here but leave
# it to the app wrapper:
run = lambda: red.connect()
main = lambda: run_app(run, flags=Flags)


if __name__ == '__main__':
    main()

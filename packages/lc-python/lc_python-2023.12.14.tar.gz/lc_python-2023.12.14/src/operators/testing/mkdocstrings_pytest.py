# deprectaed - done now in auto_docs.py, pre build. Took too long

# """
# This module is adding pytest results to the standard python handler.

# which collects data with [`pytkdocs`](https://github.com/pawamoy/pytkdocs).
# """

# import os

# os.environ['gevent_no_patch'] = 'true'  # noqa
# from operators.testing.auto_docs import dir_pytest_base  # noqa
# from devapp.tools import project, read_file, write_file
# from mkdocstrings.handlers import python
# from typing import Any, List, Optional
# import logging


# log = logging.getLogger('mkdocs.extension.pytest')


# exists = os.path.exists
# get_handler = python.get_handler

# # the foo.bar in '::: foo.bar' in markdown page, i.e. the module we collect stuff from
# current_ident = [0]

# # first monkey patch: We need the ident for the images links:
# def my_collector(self, ident, config):
#     current_ident[0] = ident
#     return self.orig_collect(ident, config)


# python.PythonCollector.orig_collect = python.PythonCollector.collect
# python.PythonCollector.collect = my_collector


# def is_test(child):
#     if child['name'].startswith('test'):
#         return True


# def rebuild_category_lists(obj: dict) -> None:
#     """
#     A copy of the original function with adding our pytest results
#     """
#     for category in ('attributes', 'classes', 'functions', 'methods', 'modules'):
#         obj[category] = [obj['children'][path] for path in obj[category]]
#     obj['children'] = [child for _, child in obj['children'].items()]
#     for child in obj['children']:
#         cat = child['category']
#         if cat in ('function', 'method') and is_test(child):
#             insert_test_results(child)
#         rebuild_category_lists(child)


# # monkey patch:
# python.orig_rebuild = python.rebuild_category_lists
# python.rebuild_category_lists = rebuild_category_lists


# def find_test_log_dir(fp, name, parent):
#     n, d_pre = name, dir_pytest_base + fp + '::'
#     d = d_pre + n
#     if exists(d):
#         return d

#     d1 = d_pre + parent.rsplit('.', 1)[-1] + '::' + n
#     if exists(d1):
#         return d1


# details = '''

# <details>
#     <summary>%s</summary>
#     %s
# </details>

#     '''


# def insert_test_results(child):
#     """child a function or method, detected to be starting with "test_"
#     -> look for test logs and insert
#     """
#     fp = child['file_path']
#     log.debug('Inserting test flows for %s' % fp)
#     d = find_test_log_dir(fp, child['name'], child['parent_path'])
#     if not d:
#         l = log.debug if 'lc:noflow' in str(child['source']) else log.warning
#         l('%s: No tests found.' % fp)
#         return
#     sects = child['docstring_sections']
#     add = lambda md, i=1, s=sects: s.insert(i, {'type': 'markdown', 'value': md})
#     add('', i=0) if not sects else 0
#     ls = os.listdir
#     posts = [f for f in ls(d) if f.startswith('flow.post') and f.endswith('.json')]
#     fns = os.path.basename(d)
#     for post in posts:
#         n = post.split('flow.post.', 1)[1].split('.json')[0]
#         flow_post = read_file(d + '/' + post, dflt='')
#         if flow_post:
#             fng = post.replace('flow.post', 'graph_easy.post').rsplit('.json', 1)[0]
#             g = '![](./auto_img/%s_%s.svg)' % (fns, fng)
#             c = '\n```js\n%s\n```\n' % flow_post
#             add(details % ('flow post build: tab ' + n, '\n'.join([g, c])))

#     flow_pre = read_file(d + '/flow.pre.json', dflt='')
#     if flow_pre:
#         c = '\n```js\n%s\n```\n' % flow_pre
#         add(details % ('flow', c))
#         add('![](./auto_img/%s_graph_easy.pre.svg)' % fns)
#     else:
#         log.warn('no test log found: %s. Run export write_build_log=pytest; pyest' % d)
#     child['name'] = child['name'].replace('test_', '')
#     child['signature'] = {'parameters': []}

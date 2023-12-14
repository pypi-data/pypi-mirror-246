# This package

<!-- badges -->

[![docs pages][docs pages_img]][docs pages] [![gh-ci][gh-ci_img]][gh-ci] [![pkg][pkg_img]][pkg] [![code_style][code_style_img]][code_style]

[docs pages]: http://klessinger.pages.axiros.com/lc-python
[docs pages_img]: ./img/badge_docs.svg
[gh-ci]: https://gitlab.axiros.com/klessinger/lc-python/actions/workflows/ci.yml
[gh-ci_img]: https://gitlab.axiros.com/klessinger/lc-python/actions/workflows/ci.yml/badge.svg
[pkg]: https://artifacts.axiros.com/artifactory/pypi-ax-sources/lc-python/2021.6.2/lc-python-2021.6.2.tar.gz
[pkg_img]: ./img/badge_pypi.svg
[code_style]: https://pypi.org/project/axblack/
[code_style_img]: ./img/badge_axblack.svg

<!-- badges -->

[![docs][img_docs]][lnk_docs]&nbsp; [![package][img_package]][lnk_package]&nbsp; [![discuss][img_discuss]][lnk_discuss]&nbsp; [![pipeline][img_pipeline]][lnk_pipeline]&nbsp; [![code style][img_code style]][lnk_code style]

[lnk_docs]: http://devapps.pages.axiros.com/lc-python
[img_docs]: https://axchange.axiros.com/scm/hg/noauth/badges/raw-file/a2d5751cb09c/lc-python/documentation.svg
[lnk_package]: https://artifacts.axiros.com/artifactory/pypi-ax-sources/lc-python/2020.12.09/lc-python-2020.12.09.tar.gz
[img_package]: https://axchange.axiros.com/scm/hg/noauth/badges/raw-file/a2d5751cb09c/lc-python/pypi_package.svg
[lnk_discuss]: https://join.skype.com/krSNYZqvEmJm
[img_discuss]: https://axchange.axiros.com/scm/hg/noauth/badges/raw-file/a2d5751cb09c/lc-python/discuss.svg
[lnk_pipeline]: https://gitlab.axiros.com/devapps/lc-python/-/commits/master
[img_pipeline]: https://axchange.axiros.com/scm/hg/noauth/badges/raw-file/a2d5751cb09c/lc-python/pipeline.svg
[lnk_code style]: https://github.com/axiros/axblack
[img_code style]: https://axchange.axiros.com/scm/hg/noauth/badges/raw-file/a2d5751cb09c/lc-python/code_style_ax_black.svg

## About
![](img/page-teaser.png){: style="width:1550px"}

Axiros Low Code Platform (AX/LC) allows for the building of complex data processing pipelines, from

- an extendable set of small building blocks (operator functions)
- a declarative, composable description file, which can be editted e.g. visually.

> An often drawn analogy to that approach is the one with Lego, which also allows to build complex designs, based on a set of generic and some design specifig blocks, plus a manual, describing how to put them together - while still allowing customization to a large extent.

### This Package

This is the core package for the Axiros Low Code Platform.

It contains:

- The base platform ops and dev command line tools
- The python reference implementation of the AX/LC data pipeline building protocol
- The `ax.core` operator namespace, containing basic generic building blocks
- The javascript running within Node-RED, enabling the AX/LC pipeline building protocol on Node-RED side.

---

Last modified: Fri Dec 18 17:10:06 2020

<!-- pre_proc_marker -->

---

??? warning "Documentation was built with development versions of libs!"

    - [lc-python](git@gitlab.axiros.com:devapps/lc-python.git)
    ```
    commit d06dbfa5a40cf8c0564a6eb26a43e81b4888a7ab
    Author: Gunther Klessinger <gk@axiros.com>
    Date:   Sat Jan 30 16:25:17 2021 +0100

        ci: trigger CI (empty commit)

    commit 23bdaa68dacb7d040414eff41a158ce3504e960e
    Author: Gunther Klessinger <gk@axiros.com>
    Date:   Sat Jan 30 15:54:00 2021 +0100

        fix: No capture at tests
    ```

    - [lc-devapp](git@gitlab.axiros.com:devapps/lc-devapp.git)
    ```
    commit 520081be6a9c5181c60c80fa27f090edeb438ea7
    Author: Gunther Klessinger <gk@axiros.com>
    Date:   Sat Jan 30 18:16:42 2021 +0100

        feat: ops lc can now kill services of other processes

        ...and also supports s for start

    commit 8b55380fe7ec718ec78358bcda0792686884a526
    Author: Gunther Klessinger <gk@axiros.com>
    Date:   Sat Jan 30 12:45:23 2021 +0100

        chore: better output
    ```

    - [lc-doctools](git@gitlab.axiros.com:devapps/lc-doctools.git)
    ```
    commit ad5dd751b688d1a64d7eb4534f0a393f14c9d89c
    Author: Gunther Klessinger <gk@axiros.com>
    Date:   Thu Jan 21 11:05:21 2021 +0100

        fix: flow -flows

    commit 161cfd0b0ceb63889687ef897a9aa357352408fc
    Author: Gunther Klessinger <gk@axiros.com>
    Date:   Wed Jan 20 23:43:46 2021 +0100

        fix: keep path in tmux
    ```

Last modified: Sun Jan 31 00:59:16 2021

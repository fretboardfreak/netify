=================
netify change-log
=================

- **0.3**: TBD

  - use distutils commands to run tests and code checkers. The script
    ``style.sh`` has been replaced with four setuptools commands:

    - "pep8": run pep8 on all source files
    - "pylint": run pylint on all source files
    - "unittest": run available unittests in "netify.tests" package.
    - "test": run the "pep8", "pylint" and "unittest" commands all together.

  - introduce unit testing framework

  - additional tweaks and updates to the RawFile view.

    - sorted directory listing page.
    - hide parent dir link when it matches the top dir link.

- **0.2**: 160910 - Raw Files

  - add a change log: CHANGES.rst

  - add message flashing support to the HtmlPage base template and HelloWorld
    View.

  - add a Raw File view to serve a directory of RST and TXT files in raw form.

- **0.1.1**: 160908 - Rebuild to fix a rookie mistake

- **0.1**: 160908 - First PyPI release

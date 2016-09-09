==========
**netify**
==========

**netify** is a library/application/framework that tries to make it easier for you
to create something for the internet.

The goal of **netify** is to make it easy to customize your own website. You can
build a web application with server side elements responding to user sessions
or compose some of your files into a static website for
upload to a hosting service. **netify** should offer something to make your task a
little bit easier.

In the most basic sense, **netify** provides a solid structure for starting up a
new `Flask <http://flask.pocoo.org/>`_ project quickly. Beyond that, **netify**
tries to provide useful tools for creating your own custom wesite or
application with minimal effort. Use it as a library in your python application
to add a web based UI that can be deployed with `docker
<https://www.docker.com>`_. Or, use it directly as an application to compose a
few of the features provided by **netify** into a quick personalized website.

**TL;DR**: *Turn boring things into something for the net*

.. admonition:: Project Links

    - Homepage: http://fretboardfreak.com/netify
    - Mirror: http://pythonhosted.org/netify (Not Active Yet)
    - PyPi: https://pypi.python.org/pypi/netify
    - Github: https://github.com/fretboardfreak/netify
    - Bitbucket (mirror): https://bitbucket.org/fret/netify (Not Active Yet)

*Dev Note*::

    At this time I would call this an alpha quality project. netify is nearing
    the point where I can start using and maturing it rather than writing new
    infrastructure. I also plan to eventually have more in depth documentation
    covering the API of the Netify project. For now, here is a summary to wet
    your appetite.

    Pull requests, feedback, and defect submissions are both accepted and
    encouraged throughout this early forming process so don't be shy!

    --fretboardfreak
    :date: 160908


Getting Started
---------------

*TBD*

Code Structure
--------------

The following module dependency diagram roughly describes the current structure
of Netify::

    [front_end_script]
            |
      [netify.app]---------\
            |              |
      [netify.config]   [netify.view]
            |              |
        [config.cfg]   [netify.template]

- Front End Script: The front end script imports or composes a Netify
  application object through multiple inheritance of the Netify Mixin classes,
  then calls the appropriate main method to start the application.

Modules from the **netify** package:

- **app**: A module containing mixin classes that can be composed to create a
  Netify app with the features you require in your project.

- **config**: Contains a config class and required helper code for reading an
  INI based config file and retrieving the configuration in a way that is
  most useful for the application.

- **config.cfg**: An INI formatted configuration file. The default sections
  are:

  - *flask*: used to hold Flask configuration instead of Flask's mechanism. I'd
    rather only have one config file.

  - *netify_views*: A section to help configure the views available in the
    application.

  - *routes*: A section mapping view classes to the base route used for those
    views in the application.

  - *other*: Some views can be configured here too. The section name for the
    view should match the name used for the "netify_views:enabled" option.

- **view**: Using the `Flask Classy <http://pythonhosted.org/Flask-Classy/>`_
  extension this module provides a base View class for Netify applications. The
  plan is to also include a set of configurable view classes that can be
  modularly composed together. It is still encouraged for users of this package
  to write some of their own templates or views, the code here should serve as
  an example of how to use the Netify library.

- **template**: A module (soon to be package) that adds some flexibility into
  your templating life. While it will also support standard, file based `Jinja
  <http://jinja.pocoo.org/>`_ templating, the Netify.template module also
  includes support for, and examples of, templates created purely in code - or
  by a combination of traditional and code based methods - using the `Yattag
  <http://www.yattag.org/>`_ library.

Contributing
============

The code is written for python 3 and the ``style.sh`` script has been
implemented to keep an eye on my coding style. I would prefer not to ignore any
of the messages from either the ``pep8`` or the ``pylint`` tool.

Trailing whitespace is a no-no so get rid of it all. :)

Beyond that, I prefer explicit over implicit, which is one of the strong
pricipals driving the design of Netify to begin with. An example of this design
is the way that the NetifyApp requires instanciation by some front end starting
script. In contrast, a typical Flask app just puts the instantiation code at
module level somewhere in the codebase. Ugh, the animals! :)

Pull requests, feedback, and defect submissions are accepted and encouraged!

License
=======

Netify uses the Apache Version 2.0 License. Please see ``LICENSE.rst`` for
more information::

    Copyright 2016 Curtis Sand

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.


.. EOF README

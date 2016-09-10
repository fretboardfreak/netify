# Copyright 2015 Curtis Sand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Flask view objects for the netify app."""

import os
from enum import Enum

from flask import url_for
from flask import flash
from flask import Markup
from flask_classy import FlaskView
from yattag import Doc

from .template import HtmlPage
from .template import build_debug_div
from .template import list_to_html_list


class NetifyView(FlaskView):
    """A View class for use with Netify applications."""
    name = "netify_view"
    netify_app = None

    @classmethod
    def register(cls, netify_app, **kwargs):
        """Register this view against the Netify Web Application."""
        cls.netify_app = netify_app
        super(NetifyView, cls).register(netify_app.flask_app, **kwargs)

    @property
    def page_options(self):
        """Retrieve the options for this View from the config file."""
        return self.netify_app.config.get_page_options(self.name)


class HelloWorld(NetifyView):
    """A Hello World index view example with debugging output."""
    name = 'hello_world'
    route_base = '/'

    def index(self):
        """Handle an incoming request for a route registered to this View."""
        hello_world = 'Hello World From Netify'
        debug = False
        if 'debug' in self.page_options:
            debug = self.page_options['debug']
        if debug:
            body = Doc()
            body.text(hello_world)
            body.stag('hr')
            body.text('View Functions:')
            body.stag('br')
            body.asis(build_debug_div(self.netify_app))
            body_txt = body.getvalue()
        else:
            body_txt = hello_world
        flash('This is what a flashed message looks like: %s' % hello_world)
        flash_messages = self.page_options.get('flash_messages', False)
        return HtmlPage(head=None, body=body_txt,
                        flash_messages=flash_messages).render_template()


class RawFile(NetifyView):
    """View a directy of files in raw form in your browser."""
    name = 'raw_file'
    route_base = '/raw_file'

    @property
    def path(self):
        """Get the path of the director of files to serve."""
        return self.page_options.get('path', '')

    @property
    def dirname(self):
        """Return the name of the top level directory."""
        return os.path.split(self.page_options.get('path', ''))[1]

    def _get_display_name(self, name):
        """Return a name that can be displayed to represent the shown file."""
        if not name:
            return self.dirname
        val = os.path.join(self.dirname, name)
        if val.endswith('|'):
            return val[-1]
        return val

    def _get_safe_base_path(self, path):
        """Get a relative path that is safe to show a user."""
        base = path.replace(os.path.commonprefix([self.path, path]), '')
        if base.startswith('/'):
            base = base[1:]
        return base

    @staticmethod
    def _get_top_dir_link():
        """Get a link to the Top Directory of the Raw File view."""
        doc = Doc()
        with doc.tag('a'):
            doc.attr(href=url_for('RawFile:index'))
            doc.text('Top Dir')
        return doc.getvalue()

    @staticmethod
    def _get_parent_dir_link(parent_dir):
        """Get a link to the parent directory of the current page."""
        doc = Doc()
        with doc.tag('a'):
            if parent_dir == "":
                doc.attr(href=url_for('RawFile:index'))
            else:
                doc.attr(href=url_for('RawFile:get',
                                      name=parent_dir.replace('/', '|')))
            doc.text('Parent Dir')
        return doc.getvalue()

    def _get_navigation_links(self, path):
        """Build a list of HTML links for navigation."""
        links = []
        base = self._get_safe_base_path(path)
        if base != "":
            links.append(self._get_top_dir_link())
        parent_dir = os.path.split(base)[0]
        links.append(self._get_parent_dir_link(parent_dir))
        return list_to_html_list(links)

    def _get_dir_listing(self, path):
        """Build an HTML list of the directory contents."""
        all_fnames = [f for f in os.listdir(path)
                      if not f.startswith('.')]
        suffixes = self.page_options.get('suffix_whitelist', '').split(',')
        fnames = []
        for fname in all_fnames:
            for suffix in suffixes:
                if fname.endswith(suffix):
                    fnames.append(fname)
                    break
                elif os.path.isdir(os.path.join(path, fname)):
                    fnames.append(fname + '/')
                    break
        base = self._get_safe_base_path(path)
        links = []
        for name in fnames:
            doc = Doc()
            name = os.path.join(base, name)
            with doc.tag('a'):
                doc.attr(href=url_for('RawFile:get',
                                      name=name.replace('/', '|')))
                doc.text(name)
            links.append(doc.getvalue())
        return list_to_html_list(links)

    @staticmethod
    def _get_file(path):
        """Return the contents of a file as a preformatted text field."""
        doc = Doc()
        with doc.tag('pre'):
            with open(path, 'r') as fin:
                doc.asis(Markup.escape(fin.read()))
        return doc.getvalue()

    def _raw_file(self, name=None):
        """Build up a page for the Raw File view."""
        name = name if name else ''
        name = name.replace('|', '/')
        display_name = self._get_display_name(name)
        if 'path' not in self.page_options:
            body_txt = 'No directory to serve in the config file.'
        else:
            path = os.path.join(self.path, name)
            body = Doc()
            with body.tag('h1'):
                body.text('File: %s' % display_name)
            with body.tag('div'):
                body.attr(klass='navigation')
                body.asis(self._get_navigation_links(path))
            with body.tag('div'):
                body.attr(klass='files')
                if os.path.exists(path):
                    if os.path.isdir(path):
                        body.asis(self._get_dir_listing(path))
                    else:
                        body.asis(self._get_file(path))
            body_txt = body.getvalue()
        flash_messages = self.page_options.get('flash_messages', True)
        return HtmlPage(head=None, body=body_txt,
                        flash_messages=flash_messages).render_template()

    def index(self):
        """Get the Top Directory listing."""
        return self._raw_file()

    def get(self, name):
        """Display a file or directory given by name."""
        return self._raw_file(name=name)


class Views(Enum):
    """Enum of view classes available in this module."""
    hello_world = HelloWorld
    raw_file = RawFile

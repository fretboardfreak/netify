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

from enum import Enum

from flask.views import View
from yattag import Doc

from .template import render_template
from .template import HtmlPage
from .template import dict_to_html_list


class HelloWorldIndex(View):
    """The index view."""
    name = 'index'
    default_route = '/'

    def __init__(self, netify_app, debug=False):
        self.netify_app = netify_app
        self.debug = debug

    @classmethod
    def register(cls, netify, route=None, *args, **kwargs):
        """Register the view on the flask application."""
        if not route:
            route = cls.default_route
        netify.flask_app.add_url_rule(
            route, view_func=cls.as_view(cls.name, netify_app=netify,
                                         *args, **kwargs))

    def dispatch_request(self):
        """Handle an incoming request for a route registered to this View."""
        hello_world = 'Hello World From Netify'
        if not self.debug:
            body_txt = hello_world
        else:  # add the debug div to the bottom of the page
            body = Doc()
            body.text(hello_world)
            body.stag('hr')
            body.asis(self.debug_div)
            body_txt = body.getvalue()
        return render_template(HtmlPage(
            head=None, body=body_txt).build())

    @property
    def debug_div(self):
        """Generate a div section containing debugging information."""
        config_dict = self.netify_app.config.to_string_dict()
        div = Doc()
        with div.tag('div'):
            div.attr(klass="debug")
            div.text('DEBUG:')
            div.stag('br')
            div.text('Netify Config File:')
            div.stag('br')
            div.asis(dict_to_html_list(config_dict))
            div.stag('br')
            div.text('Flask Config')
            div.stag('br')
            div.asis(dict_to_html_list(dict(self.netify_app.flask_app.config)))
        return div.getvalue()


class Views(Enum):
    """Enum of view classes available in this module."""
    hello_world_index = HelloWorldIndex

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

from .template import render_template
from .template import HtmlPage


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
        return render_template(HtmlPage(
            head=None, body='Hello World From Netify').build())


class Views(Enum):
    """Enum of view classes available in this module."""
    hello_world_index = HelloWorldIndex

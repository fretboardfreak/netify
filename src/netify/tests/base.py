"""Basic common tools for testing netify."""
# Copyright 2016 Curtis Sand
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
import unittest

import flask_testing

import netify.app as app


class BasicTest(unittest.TestCase):
    """A base class for netify tests that do not require the netify app."""
    pass


class NetifyTest(flask_testing.TestCase):
    """A base class for netify tests that require the netify/flask app."""

    def create_app(self):
        """Create an instance of the flask_app for the Flask Testing API."""
        napp = app.NetifyApp()
        return napp.flask_app

"""The netify application object."""
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
from flask import Flask


class NetifyApp(object):
    """The Netify Application object."""
    flask_app = None

    def __init__(self, config=None):
        if self.flask_app is None:
            self.__class__.flask_app = Flask(__name__)
        if config and self.flask_app:
            config.update_flask(self.flask_app)

    def register_views(self, views):
        """Register the view classes against the flask app."""
        for view in views:
            view.register(self.flask_app)

    def run(self, host=None, port=None, debug=None):
        """Run the Flask Server."""
        self.flask_app.run(host, port, debug)

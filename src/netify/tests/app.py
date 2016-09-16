"""Tests for the netify.app module."""
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
from unittest import main
from unittest import skip
from unittest.mock import Mock
from unittest.mock import patch

import netify
import netify.app as app
import netify.config as config

from .base import NetifyBaseTest


class TestNetifyCore(NetifyBaseTest):
    """Tests for the netify.app module."""

    def test_singleton(self):
        """Verify that NetifyApp is a signleton."""
        self.assertEqual(app.NetifyApp().flask_app, self.app)

    @staticmethod
    @patch('netify.app.NetifyApp.configure')
    def test_init_config(mock_configure):
        """Test that the configure method is called passed to constructor."""
        app.NetifyApp(config=Mock())
        mock_configure.assert_called()

    def test_description(self):
        """Verify the string description property of the netify object."""
        napp = app.NetifyApp()
        self.assertIsInstance(napp.description, str)

    @patch('netify.config.Config.update_flask')
    @patch('netify.config.SafeConfigParser', Mock())
    def test_configure_path(self, mock_update_flask):
        """Verify the configure method accepts a config path."""
        path = 'some/fake/path'
        napp = app.NetifyApp()
        napp.configure(path)
        self.assertIsInstance(napp.config, config.Config)
        self.assertTrue(mock_update_flask.called)

    @patch('netify.config.Config.update_flask')
    @patch('netify.config.SafeConfigParser', Mock())
    def test_configure_obj(self, mock_update_flask):
        """Verify the configure method accepts a config object."""
        config_obj = config.Config('blah/blah/blah')
        napp = app.NetifyApp()
        napp.configure(config_obj)
        self.assertEqual(napp.config, config_obj)
        self.assertTrue(mock_update_flask.called)

    @staticmethod
    @patch.object(netify.app.NetifyApp, 'flask_app')
    def test_run(mflask_app):
        """Verify the run method behaves as expected."""
        host = 'host'
        port = 8080
        debug = True
        napp = app.NetifyApp()
        napp.run(host, port, debug)
        mflask_app.run.assert_called_once_with(host, port, debug)

    @skip('Not implemented yet')
    def test_register_views(self):
        """Verify the process of registering Flask views."""
        pass


if __name__ == "__main__":
    main()

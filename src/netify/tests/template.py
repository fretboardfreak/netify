"""Tests for the netify template module."""
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
from unittest.mock import patch
from unittest.mock import Mock
import abc

import yattag

from netify.tests.base import NetifyBaseTest
import netify.template as template


class RenderTemplateTest(NetifyBaseTest):
    """Test that the template module's methods work as expected."""

    @staticmethod
    @patch('netify.template.Markup')
    @patch('netify.template.render_template_string')
    def test_render_template_string(mock_rts, mock_markup):
        """Verify that render_template accepts a string template."""
        test_string = 'some string'
        template.render_template(test_string)
        mock_rts.assert_called_once_with(test_string)
        mock_markup.assert_called_once_with(mock_rts(test_string))

    @staticmethod
    @patch('netify.template.Markup')
    @patch('netify.template.render_template_string')
    def test_render_template_doc(mock_rts, mock_markup):
        """Verify that render_template accepts a yattag Doc template."""
        test_string = 'some string'
        test_doc = Mock(spec=yattag.Doc)
        test_doc.getvalue.return_value = test_string
        template.render_template(test_doc)
        test_doc.getvalue.assert_called_once_with()
        mock_rts.assert_called_once_with(test_string)
        mock_markup.assert_called_once_with(mock_rts(test_string))


class PageTest(NetifyBaseTest):
    """Test the Page base class."""

    def test_is_abstract_base_class(self):
        """Check that template.Page is an abstract base class."""
        self.assertIsInstance(template.Page, abc.ABCMeta)

    def test_build(self):
        """Verify that a the abstract method "build" is present."""
        self.assertTrue(hasattr(template.Page, 'build'))
        self.assertTrue(
            hasattr(template.Page.build, '__isabstractmethod__') and
            getattr(template.Page.build, '__isabstractmethod__', False))

    @staticmethod
    @patch('netify.template.render_template')
    def test_render_template(mock_render_template):
        """Test that the Page object can render itself."""
        mock_self = Mock()
        template.Page.render_template(mock_self)
        mock_self.build.assert_called_once_with()
        mock_render_template.assert_called_once_with(mock_self.build())

    @staticmethod
    def test__call__():
        """Test the behaviour of the call magic method."""
        mock_self = Mock()
        template.Page.__call__(mock_self)
        mock_self.build.assert_called_once_with()

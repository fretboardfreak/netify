"""Generate Jinja2 Templates and/or HTML pages programmatically."""
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
from flask import Markup
from flask import render_template_string
from yattag import Doc


def render_template(template):
    """Run a template through Jinja2 and make it safe for the web.

    :param template: Either a string or yattag.Doc object.
    """
    if isinstance(template, Doc):
        template_string = template.getvalue()
    else:
        template_string = template
    return Markup(render_template_string(template_string))


class Page(object):
    """Base object for pages."""
    def build(self):
        """Build the page template string."""
        raise NotImplementedError('%s: Must be implemented by subclass.' %
                                  self.__class__.__name__)

    def __call__(self, *args, **kwargs):
        self.__class__.__init__(self, *args, **kwargs)
        return self.build()


class HtmlPage(Page):
    """Build an HTML Page with the given head and body content.

    :param head: Either a string or yattag.Doc object representing the page's
                 head section. If not otherwise provided the default header
                 will contain only the charset meta tag.

    :param body: Either a string or yattag.Doc object representing the page's
                 body section.

    """
    object_string_map = {'head': 'head_txt', 'body': 'body_txt'}

    def __init__(self, head=None, body=None):
        if head is not None:
            self.head = head
        if body is not None:
            self.body = body
        self.head_txt = None
        self.body_txt = None

    def _get_text(self):
        """Convert possible yattag.Doc objects to strings."""
        for obj_name in self.object_string_map:
            obj = getattr(self, obj_name, '')
            obj = '' if obj is None else obj
            if isinstance(obj, Doc):
                setattr(self, self.object_string_map[obj_name],
                        obj.getvalue())
            else:
                setattr(self, self.object_string_map[obj_name], obj)

    def build(self):
        if getattr(self, 'head', '') in ['', None]:
            self.head = Doc()
            self.head.stag('meta', charset='utf-8')
        self._get_text()
        doc = Doc()
        doc.asis('<!DOCTYPE html/>')
        with doc.tag('html'):
            doc.attr(lang='en')
            with doc.tag('head'):
                doc.asis(self.head_txt)
            with doc.tag('body'):
                doc.asis(self.body_txt)
        return doc

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
import abc

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


class Page(abc.ABC):
    """Base object for pages."""
    @abc.abstractmethod
    def build(self):
        """Build and return the page template string."""
        pass

    def render_template(self):
        """Helper method for rendering a page template."""
        return render_template(self.build())

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

    def __init__(self, head=None, body=None, flash_messages=True):
        if head is not None:
            self.head = head
        if body is not None:
            self.body = body
        self.head_txt = None
        self.body_txt = None
        self.flash_messages = flash_messages

    def get_text(self):
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
        self.get_text()
        doc = Doc()
        doc.asis('<!DOCTYPE html/>')
        with doc.tag('html'):
            doc.attr(lang='en')
            with doc.tag('head'):
                doc.asis(self.head_txt)
            with doc.tag('body'):
                doc.asis(self.body_txt)
                if self.flash_messages:
                    doc.asis(get_flashed_messages_div())
        return doc


def dict_to_html_list(dictionary, key_sep=None):
    """Convert a python dictionary into a string representing an HTML list."""
    key_sep = ': ' if not key_sep else key_sep
    doc = Doc()
    if not dictionary:
        return ""
    with doc.tag('ul'):
        for key in dictionary:
            with doc.tag('li'):
                if isinstance(dictionary[key], dict):
                    doc.text('%s%s' % (key, key_sep))
                    doc.asis(dict_to_html_list(dictionary[key]))
                elif isinstance(dictionary[key], (list, tuple)):
                    doc.asis(list_to_html_list(dictionary[key]))
                else:
                    doc.text('%s%s%s' % (key, key_sep, dictionary[key]))
    return doc.getvalue()


def list_to_html_list(iterable, list_tag=None):
    """Convert a python list into a string representing an HTML list."""
    list_tag = list_tag if list_tag else 'ul'
    if not iterable:
        return ""
    doc = Doc()
    with doc.tag(list_tag):
        for item in iterable:
            with doc.tag('li'):
                if isinstance(item, dict):
                    doc.asis(dict_to_html_list(item))
                elif isinstance(item, (list, tuple)):
                    doc.asis(list_to_html_list(item))
                else:
                    doc.asis(item)
    return doc.getvalue()


def build_debug_div(netify):
    """Generate a div section containing debugging information."""
    config_dict = netify.config.to_string_dict()
    div = Doc()
    with div.tag('div'):
        div.attr(klass="debug")
        div.text('DEBUG:')
        rules = {}
        for rule in list(netify.flask_app.url_map.iter_rules()):
            rules[rule.endpoint] = rule.rule
        div.asis(dict_to_html_list(rules, key_sep=' - '))
        div.stag('br')
        div.text('Netify Config File:')
        div.stag('br')
        div.asis(dict_to_html_list(config_dict))
        div.stag('br')
        div.text('Flask Config')
        div.stag('br')
        div.asis(dict_to_html_list(dict(netify.flask_app.config)))
    return div.getvalue()


def get_flashed_messages_div():
    """Build and fill a div tag with any flashed messages.,

    This is just a jinja2 template for retrieving flashed messages. The
    render_template method still needs to be called to get any messages
    that are flashed before sending the page to the client.
    """
    doc = Doc()
    with doc.tag('div'):
        doc.asis('{% with messages = get_flashed_messages() %}')
        doc.asis('{% if messages %}')
        doc.asis('<hr>')
        doc.text('Messages')
        doc.asis('<ul class=flashes>')
        doc.asis('{% for message in messages %}')
        doc.asis('<li>{{ message }}</li>')
        doc.asis('{% endfor %}')
        doc.asis('</ul>')
        doc.asis('{% endif %}')
        doc.asis('{% endwith %}')
    return doc.getvalue()

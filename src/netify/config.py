"""Configuration for netify."""
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
import os
from configparser import SafeConfigParser
from enum import Enum


def guess_a_config_location():
    """Try to look for a netify config file in a few appropriate places."""
    names = ['netify.cfg', 'config.cfg', 'dev.cfg']
    home_paths = [os.path.join(os.getenv('HOME'), stub)
                  for stub in ['.%s', 'netify/%s']]
    other_paths = ['/etc/netify/%s']
    paths = [os.path.join(os.getcwd(), name) for name in names]
    paths.append('/etc/netify.cfg')
    for name in names:
        paths.extend(path % name for path in home_paths)
    for name in names:
        paths.extend(path % name for path in other_paths)
    return [path for path in paths if os.path.exists(path)]


class Section(Enum):
    """String names for the sections in the Netify config file"""
    flask = 'flask'
    netify_views = 'netify_views'
    routes = 'routes'


class Config(object):
    """The config object providing access to Netify configuration."""
    _instance = None  # storage on the class for the singleton
    default_secret_key_size = 64  # 64 bytes => 512 bits

    def __init__(self, config_file):
        self.file = config_file
        self.parser = SafeConfigParser()
        if isinstance(self.file, (str, list)):
            self.parser.read(self.file)
        else:  # assume file object was given instead
            self.parser.read_file(self.file)

    @classmethod
    def load_config(cls, config_file):
        """Load the configuration singleton object from the given file."""
        cls._instance = cls(config_file)
        return cls._instance

    def get(self, *args, **kwargs):
        """Get an Option from one of the Config Sections."""
        return self.parser.get(*args, **kwargs)

    def to_string_dict(self):
        """Return the whole config as a dictionary of string key values.

        All keys and values are strings, as written int he config file.
        """
        ret_val = {}
        for section in self.parser.sections():
            for option in self.parser.options(section):
                sect = ret_val.get(section, {})
                sect[option] = self.parser.get(section, option)
                ret_val[section] = sect
        return ret_val

    @classmethod
    def get_random_secret_key(cls, size=None):
        """Generate a random secret key string."""
        if not size:
            size = cls.default_secret_key_size
        return os.urandom(size)

    @property
    def flask_config_dict(self):
        """Parse the config file and create a dict compatible with Flask."""
        flask_config = dict([(obj.name, obj.value) for obj in FlaskDefaults])
        for option in self.parser.options(Section.flask.value):
            flask_config[option.upper()] = self.get(Section.flask.value,
                                                    option)
        return flask_config

    def update_flask(self, flask_app):
        """Add the options from the Flask section into the flask object."""
        flask_app.config.update(self.flask_config_dict)

    def _section_as_dict(self, section):
        views = {}
        for option in self.parser.options(section):
            # Don't know which options might be boolean so we can't use
            # self.parser.getboolean()
            tmp = self.get(section, option)
            if str(tmp).lower() in ['yes', 'y', 'true', 't']:
                views[option] = True
            elif str(tmp).lower() in ['no', 'n', 'false', 'f']:
                views[option] = False
            else:
                views[option] = str(tmp)
        return views

    @property
    def netify_views(self):
        """Get the 'netify_views' section."""
        return self._section_as_dict(Section.netify_views.value)

    def get_page_options(self, name):
        """Return a dict of options for a page."""
        return self._section_as_dict(name)

    @property
    def routes(self):
        """Return the routes section from the config file."""
        return self._section_as_dict(Section.routes.value)


class FlaskDefaults(Enum):
    """Default values for the Flask section of the config file."""
    SECRET_KEY = Config.get_random_secret_key()
    LOGGER_NAME = 'netify'

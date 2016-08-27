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


class Section(Enum):
    """String names for the sections in the Netify config file"""
    flask = 'flask'


class Config(object):
    """The config object providing access to Netify configuration."""
    _instance = None  # storage on the class for the singleton
    default_secret_key_size = 64  # 64 bytes => 512 bits

    def __init__(self, config_file):
        self.file = config_file
        self.parser = SafeConfigParser()
        if isinstance(self.file, str):
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


class FlaskDefaults(Enum):
    """Default values for the Flask section of the config file."""
    SECRET_KEY = Config.get_random_secret_key()
    LOGGER_NAME = 'netify'

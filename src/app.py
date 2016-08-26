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

"""The netify application object."""

import os

from flask import Flask

DEFAULT_SECRET_KEY_SIZE = 64  # bytes -> 64 * 8 = 512bits

APP = Flask(__name__)
APP.config.from_object(__name__)
APP.config.update(dict(SECRET_KEY=os.urandom(DEFAULT_SECRET_KEY_SIZE)))

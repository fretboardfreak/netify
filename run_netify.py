#!/usr/bin/env python
"""The development netify CLI script."""
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
import sys

# Modify the path to add the "src" directory. This lets netify be imported
# later down in the protected "__main__" block below.
sys.path.insert(0, './src')


def run_netify():
    """Run the CLI Main method for Netify.

    This is encapsulated in a method to appease the pylint gods. At the module
    level we need to add the "src" directory to the path so no more module
    level imports are allowed. Using a method we squish the import scope and
    get to drink our flask too.
    """
    from netify.app import NetifyApp
    NetifyApp.cli_main()


if __name__ == "__main__":
    run_netify()

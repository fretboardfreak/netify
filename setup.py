"""The netify deployment script."""
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
import distutils.log
from distutils.cmd import Command
from setuptools import setup
import os
import subprocess


def required():
    with open('requirements.txt', 'r') as reqf:
        return reqf.read().splitlines()


def readme():
    with open('README.rst', 'r') as readmef:
        return readmef.read()


class PylintCommand(Command):
    """A custom command to run Pylint on all Python source files."""

    description = "Run pylint on the netify sources."
    user_options = [
        ('pylint-rcfile=', None, 'path to Pylint config file.')
    ]

    def initialize_options(self):
        """Set defaults for options."""
        self.pylint_rcfile = ''

    def finalize_options(self):
        """Post-process options."""
        if self.pylint_rcfile:
            assert os.path.exists(self.pylint_rcfile), (
                'Cannot find config file "%s"' % self.pylint_rcfile)

    def run(self):
        """Run Pylint."""
        command = ['pylint']
        if self.pylint_rcfile:
            command.append('--rcfile=%s' % self.pylint_rcfile)
        command.append(os.path.join(os.getcwd(), 'src/netify'))
        self.announce('running command: %s' % str(command),
                      level=distutils.log.INFO)
        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError as exc:
            self.announce('Non-zero returncode "%s": %s' %
                          (exc.returncode, exc.cmd),
                          level=distutils.log.INFO)
            return 1


setup(name='netify',
      version='0.2',
      description='Turn boring things into something for the net.',
      long_description=readme(),
      url='https://github.com/fretboardfreak/netify',
      author='Curtis Sand',
      author_email='curtissand@gmail.com',
      license='Apache',
      package_dir={'': 'src'},
      packages=['netify'],
      entry_points={
          'console_scripts': ['netify=netify.app:NetifyApp.cli_main']
      },
      use_2to3=False,
      install_requires=required(),
      zip_safe=True,
      include_package_data=True,
      test_suite='netify.tests',
      keywords='net netify app webapp html site website generator',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Framework :: Flask',
          'Environment :: Web Environment',
          'Operating System :: POSIX :: Linux',
          'Operating System :: MacOS',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Internet',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Internet :: WWW/HTTP :: Site Management',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          ('Topic :: Software Development :: Libraries :: '
           'Application Frameworks'),
          ],
      cmdclass={'pylint': PylintCommand},
      )

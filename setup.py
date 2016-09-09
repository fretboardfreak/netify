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
from setuptools import setup


def required():
    with open('requirements.txt', 'r') as reqf:
        return reqf.read().splitlines()


def readme():
    with open('README.rst', 'r') as readmef:
        return readmef.read()


setup(name='netify',
      version='0.1.1',
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
      )

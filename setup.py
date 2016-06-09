'''
Copyright (c) 2013-2014 Hypothes.is Project and contributors

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''


# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import os

from setuptools import setup, find_packages
from setuptools.command.sdist import sdist as _sdist
from setuptools.command.test import test as TestCommand

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()


class PyTest(TestCommand):
    user_options = [
        ('cov', None, 'measure coverage')
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.cov = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['h']
        self.test_suite = True
        if self.cov:
            self.test_args += ['--cov', 'h',
                               '--cov-config', '.coveragerc']

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

INSTALL_REQUIRES = [
    'PyJWT>=1.0.0,<2.0.0',
    'SQLAlchemy>=0.8.0',
    'alembic>=0.7.0',
    'annotator>=0.14.2,<0.15',
    'blinker>=1.3,<1.4',
    'cryptacular>=1.4,<1.5',
    'cryptography>=0.7',
    'deform>=0.9,<1.0',
    'deform-jinja2>=0.5,<0.6',
    'elasticsearch>=1.1.0,<2.0.0',
    'gevent>=1.0.2,<1.1.0',
    'gnsq>=0.3.0,<0.4.0',
    'gunicorn>=19.2,<20',
    'itsdangerous>=0.24',
    'jsonpointer==1.0',
    'jsonschema>=2.5.1,<2.6',
    'pyramid>=1.5,<1.6',
    'psycogreen>=1.0',
    'psycopg2>=2.6.1',
    'pyramid_mailer>=0.13',
    'pyramid_tm>=0.7',
    'python-dateutil>=2.1',
    'python-slugify>=1.1.3,<1.2.0',
    'python-statsd>=1.7.0,<1.8.0',
    'webassets>=0.10,<0.11',
    'pyramid_webassets>=0.9,<1.0',
    'pyramid-jinja2>=2.3.3',
    'raven>=5.10.2,<5.11.0',
    'requests>=2.7.0',
    'unicodecsv>=0.14.1,<0.15',
    'ws4py>=0.3,<0.4',
    'zope.sqlalchemy>=0.7.6,<0.8.0',

    # Version pin for known bug
    # https://github.com/repoze/repoze.sendmail/issues/31
    'repoze.sendmail<4.2',
]

DEV_EXTRAS = ['pyramid_debugtoolbar>=2.1', 'prospector[with_pyroma]', 'pep257',
              'sphinxcontrib-httpdomain']
TESTING_EXTRAS = ['mock>=1.3.0', 'pytest>=2.5', 'pytest-cov', 'factory-boy']
YAML_EXTRAS = ['PyYAML']

setup(name='annotran',
      version='0.0',
      description='annotran',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='annotran',
      install_requires=INSTALL_REQUIRES,
      entry_points="""\
      [paste.app_factory]
      main = annotran:main
      [console_scripts]
      initialize_annotran_db = annotran.scripts.initializedb:main
      """,
      )

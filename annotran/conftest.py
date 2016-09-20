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
# monkey patching of hypothesis methods

# annotran's version of h.conftest

# -*- coding: utf-8 -*-
# pylint: disable=no-self-use
"""
The `conftest` module is automatically loaded by py.test and serves as a place
to put fixture functions that are useful application-wide.
"""

import os

import pytest

from pyramid.paster import get_appsettings

from h.config import normalize_database_url
from h import conftest


class DummyFeature(object):

    """
    A dummy feature flag looker-upper.

    Because we're probably testing all feature-flagged functionality, this
    feature client defaults every flag to *True*, which is the exact opposite
    of what happens outside of testing.
    """

    def __init__(self):
        self.flags = {}

class DummySession(object):

    """
    A dummy database session.
    """

    def __init__(self):
        self.added = []
        self.deleted = []
        self.flushed = False


@pytest.fixture(scope='session', autouse=True)
def settings():
    """Default app settings (test.ini)."""
    settings = get_appsettings('test.ini')

    if 'TEST_DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = normalize_database_url(
            os.environ['TEST_DATABASE_URL'])

    return settings

DummySession.settings = settings

setup_database = conftest.setup_database
database_session = conftest.database_session
config = conftest.config
deform = conftest.deform
authn_policy = conftest.authn_policy
mailer = conftest.mailer
notify = conftest.notify
routes_mapper = conftest.routes_mapper
_make_session = conftest._make_session


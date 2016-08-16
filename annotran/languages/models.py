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

#this is a code reused from hypothesis, adapted and extended to be used for languages
# -*- coding: utf-8 -*-

import datetime

import sqlalchemy as sa
from sqlalchemy.orm import exc

from h.db import Base
from h import pubid

LANGUAGE_NAME_MIN_LENGTH = 4
LANGUAGE_NAME_MAX_LENGTH = 25


class Language(Base):
    __tablename__ = 'language'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    # We don't expose the integer PK to the world, so we generate a short
    # random string to use as the publicly visible ID.
    pubid = sa.Column(sa.Text(),
                      default=pubid.generate,
                      unique=True,
                      nullable=False)
    name = sa.Column(sa.UnicodeText(), nullable=False, unique=True)
    created = sa.Column(sa.DateTime,
                        default=datetime.datetime.utcnow,
                        server_default=sa.func.now(),
                        nullable=False)

    # we only need a relationship table between a language and a group
    members = sa.orm.relationship('Group',
                                  backref=sa.orm.backref('languages', lazy='dynamic'),
                                  secondary='group_language',
                                  lazy='dynamic')

    def __init__(self, name, group=None):
        self.name = name
        if group:
            self.members.append(group)

    @sa.orm.validates('name')
    def validate_name(self, key, name):
        if not LANGUAGE_NAME_MIN_LENGTH <= len(name) <= LANGUAGE_NAME_MAX_LENGTH:
            raise ValueError('name must be between {min} and {max} characters '
                             'long'.format(min=LANGUAGE_NAME_MIN_LENGTH,
                                           max=LANGUAGE_NAME_MAX_LENGTH))
        return name

    @classmethod
    def get_by_pubid(cls, pubid, page):

        """Return the language with the given pubid, or None."""
        if page:
            return cls.query.filter(cls.pubid == pubid, cls.pages.contains(page)).first()
        else:
            return None

    @classmethod
    def get_by_page(cls, page):
        """Return the language with the given pubid, or None."""
        return cls.query.filter(cls.pages.contains(page)).all()

    @classmethod
    def get_public(cls, page):
        """Return all public languages"""
        # get the current page object from the database
        # filter by page object
        return cls.query.filter(cls.members == None, cls.pages.contains(page)).all()

    @classmethod
    def get_by_id(cls, id_):
        """Return the language with the given id, or None."""
        try:
            return cls.query.filter(
                cls.id == id_).one()
        except exc.NoResultFound:
            return None

    @classmethod
    def get_by_name(cls, name):
        """Return the language with the given id, or None."""
        try:
            return cls.query.filter(
                cls.name == name).one()
        except exc.NoResultFound:
            return None

GROUP_LANGUAGE_TABLE = sa.Table(
    'group_language', Base.metadata,
    sa.Column('group_id',
              sa.Integer,
              sa.ForeignKey('group.id'),
              nullable=False),
    sa.Column('language_id',
              sa.Integer,
              sa.ForeignKey('language.id'),
              nullable=False)
)

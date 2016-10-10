"""

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
"""

# -*- coding: utf-8 -*-

import datetime

import h
import h.groups.models
import sqlalchemy as sa
from h.db import Base
from sqlalchemy.orm import exc

LANGUAGE_NAME_MIN_LENGTH = 4
LANGUAGE_NAME_MAX_LENGTH = 25


class Language(Base):
    """
    Represents a language in the database
    """
    __tablename__ = 'language'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    # We don't expose the integer PK to the world, so we generate a short
    # random string to use as the publicly visible ID.
    pubid = sa.Column(sa.Text(),
                      default=h.pubid.generate,
                      unique=True,
                      nullable=False)
    name = sa.Column(sa.UnicodeText(), nullable=False, unique=True)
    created = sa.Column(sa.DateTime,
                        default=datetime.datetime.utcnow,
                        server_default=sa.func.now(),
                        nullable=False)

    def __init__(self, name):
        """
        Initialize a language
        :param name: the name of the language
        """
        self.name = name

    @sa.orm.validates('name')
    def validate_name(self, key, name):
        """
        Validate that the language name is of an acceptable length
        :param key: the uniquely identifying key (not used)
        :param name: the name of the language
        :return: either the name or a ValueError exception
        """
        if not LANGUAGE_NAME_MIN_LENGTH <= len(name) <= LANGUAGE_NAME_MAX_LENGTH:
            raise ValueError('name must be between {min} and {max} characters '
                             'long'.format(min=LANGUAGE_NAME_MIN_LENGTH,
                                           max=LANGUAGE_NAME_MAX_LENGTH))
        return name

    @classmethod
    def get_by_public_language_id(cls, public_language_id):
        """
        Get a language with the given public language ID
        :param public_language_id: the public language ID
        :return: either a language or None
        """
        if public_language_id:
            return cls.query.filter(cls.pubid == public_language_id).first()
        else:
            return None

    @classmethod
    def get_by_id(cls, id_):
        """
        Get a language by its ID
        :param id_: the ID of the language
        :return: a language or None
        """
        try:
            return cls.query.filter(
                cls.id == id_).one()
        except exc.NoResultFound:
            return None

    @classmethod
    def get_by_name(cls, name):
        """
        Get a language by name
        :param name: the name of the language
        :return: a language or None
        """
        try:
            return cls.query.filter(
                cls.name == name).one()
        except exc.NoResultFound:
            return None

    def __repr__(self):
        """
        The internal representation of the language
        :return: the name of the language
        """
        return '{0}'.format(self.name)

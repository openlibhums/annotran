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

#this is a code reused from hypothesis, adapted and extended to be used for pages
# -*- coding: utf-8 -*-

import datetime

import sqlalchemy as sa
from sqlalchemy.orm import exc
import slugify

from h.db import Base
from h import pubid


class Language(Base):
    __tablename__ = 'page'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    uri = sa.Column(sa.Text(),
                      unique=True,
                      nullable=False)
    created = sa.Column(sa.DateTime,
                        default=datetime.datetime.utcnow,
                        server_default=sa.func.now(),
                        nullable=False)
    # we only need a relationship table between a page and a language
    members = sa.orm.relationship('Language',
                                  backref='pages',
                                  secondary='language_page')

    def __init__(self, name, group=None):
        self.name = name
        if group:
            self.members.append(group)

    @classmethod
    def get_by_uri(cls, pubid):
        """Return the page with the given uri, or None."""
        return cls.query.filter(cls.pubid == pubid).first()

    @classmethod
    def get_by_id(cls, id_):
        """Return the page with the given id, or None."""
        try:
            return cls.query.filter(
                cls.id == id_).one()
        except exc.NoResultFound:
            return None

GROUP_LANGUAGE_TABLE = sa.Table(
    'language_page', Base.metadata,
    sa.Column('language_id',
              sa.Integer,
              sa.ForeignKey('language.id'),
              nullable=False),
    sa.Column('page_id',
              sa.Integer,
              sa.ForeignKey('page.id'),
              nullable=False)
)

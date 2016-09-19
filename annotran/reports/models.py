# -*- coding: utf-8 -*-


import annotran.pages.models
import annotran.languages.models
import h.groups.models
import h.accounts.models
import sqlalchemy as sa
from h.db import Base
from sqlalchemy.orm import exc


class Report(Base):
    __tablename__ = 'report'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    page_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.pages.models.Page.id))
    page = sa.orm.relationship('Page', backref='preport')

    language_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.languages.models.Language.id))
    language = sa.orm.relationship('Language', backref='lreport')

    group_id = sa.Column(sa.Integer, sa.ForeignKey(h.groups.models.Group.id), nullable=True)
    group = sa.orm.relationship('Group', backref='greport')

    author_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id))
    author = sa.orm.relationship('User', backref='areport', foreign_keys=[author_id])

    reporter_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id))
    Reporter = sa.orm.relationship('User', backref='vreport', foreign_keys=[reporter_id])

    def __init__(self, page, language, group, author, reporter):
        if page and language and author and reporter:
            self.page_id = page.id
            self.language_id = language.id

            if group is not None:
                self.group_id = group.id
            self.author_id = author.id
            self.reporter_id = reporter.id

    @classmethod
    def get_report(cls, page, language, group, author, reporter):
        try:
            if group is None:
                return cls.query.filter(
                    cls.page_id == page.id,
                    cls.language_id == language.id,
                    cls.group_id == -1,
                    cls.author_id == author.id,
                    cls.reporter_id == reporter.id).one()
            else:
                return cls.query.filter(
                    cls.page_id == page.id,
                    cls.language_id == language.id,
                    cls.group_id == group.id,
                    cls.author_id == author.id,
                    cls.reporter_id == reporter.id).one()
        except exc.NoResultFound:
            return None

    @classmethod
    def get_by_id(cls, id_):
        """Return the report with the given id, or None."""
        try:
            return cls.query.filter(
                cls.id == id_).one()
        except exc.NoResultFound:
            return None

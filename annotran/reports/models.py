# -*- coding: utf-8 -*-


import annotran.languages.models
import annotran.pages.models
import h.accounts.models
import h.groups.models
import sqlalchemy as sa
from h.db import Base
from sqlalchemy.orm import exc


class Report(Base):
    """
    Represents an abuse report in the database
    """
    __tablename__ = 'report'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    page_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.pages.models.Page.id))
    page = sa.orm.relationship('Page', backref='page_report')

    language_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.languages.models.Language.id))
    language = sa.orm.relationship('Language', backref='language_report')

    group_id = sa.Column(sa.Integer, sa.ForeignKey(h.groups.models.Group.id), nullable=True)
    group = sa.orm.relationship('Group', backref='group_report')

    author_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id))
    author = sa.orm.relationship('User', backref='author_report', foreign_keys=[author_id])

    reporter_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id))
    Reporter = sa.orm.relationship('User', backref='reporter_report', foreign_keys=[reporter_id])

    def __init__(self, page, language, group, author, reporter):
        """
        Initialize a report
        :param page: the page to which the report corresponds
        :param language: the language to which the report corresponds
        :param group: the group to which the report corresponds
        :param author: the translation author to which the report corresponds
        :param reporter: the reporting user to which the report corresponds
        """
        if page and language and author and reporter:
            self.page_id = page.id
            self.language_id = language.id

            if group is not None:
                self.group_id = group.id
            self.author_id = author.id
            self.reporter_id = reporter.id

    @classmethod
    def get_report(cls, page, language, group, author, reporter):
        """
        Get a report by page, language, group, author, and reporter
        :param page: the page to query
        :param language: the language to query
        :param group: the group to query or None
        :param author: the author to query
        :param reporter: the reporting user to query
        :return:
        """
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
        """
        Get a report with a specific ID
        :param id_: the ID to query
        :return: a report or None
        """
        try:
            return cls.query.filter(
                cls.id == id_).one()
        except exc.NoResultFound:
            return None

    @classmethod
    def get_all(cls):
        """
        Get all reports
        :return: a list of all reports or an empty list
        """
        return cls.query.all()

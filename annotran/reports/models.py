# -*- coding: utf-8 -*-


import annotran.languages.models
import annotran.pages.models
import annotran.translations.models
import h.accounts.models
import h.groups.models
import sqlalchemy as sa
from h.db import Base
from sqlalchemy.orm import exc
from sqlalchemy import ForeignKeyConstraint


class Report(Base):
    """
    Represents an abuse report in the database
    """
    __tablename__ = 'report'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)


    page_id = sa.Column(sa.Integer)
    language_id = sa.Column(sa.Integer)
    group_id = sa.Column(sa.Integer)

    sa.ForeignKeyConstraint([page_id, language_id, group_id],
                            [annotran.translations.models.Translation.page_id,
                             annotran.translations.models.Translation.language_id,
                             annotran.translations.models.Translation.group_id])

    author_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id))
    author = sa.orm.relationship('User', backref='author_report', foreign_keys=[author_id])

    reporter_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id))
    Reporter = sa.orm.relationship('User', backref='reporter_report', foreign_keys=[reporter_id])

    def __init__(self, translation, author, reporter):
        """
        Initialize a report
        :param translation: the translation (page, group, language) to which the report corresponds
        :param author: the translation author to which the report corresponds
        :param reporter: the reporting user to which the report corresponds
        """
        if translation and author and reporter:
            self.page_id = translation.page_id
            self.language_id = translation.language_id
            self.group_id = translation.group_id
            self.author_id = author.id
            self.reporter_id = reporter.id

    @classmethod
    def get_report(cls, translation, author, reporter):
        """
        Get a report by page, language, group, author, and reporter
        :param translation: the translation (page, group, language) to which the report corresponds
        :param author: the author to query
        :param reporter: the reporting user to query
        :return:
        """
        try:
            return cls.query.filter(
                cls.page_id == translation.page_id,
                cls.language_id == translation.language_id,
                cls.group_id == translation.group_id,
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

# -*- coding: utf-8 -*-


import annotran
import annotran.languages.models as lang_models
import annotran.pages.models
import h
import h.accounts.models
import h.groups.models
import sqlalchemy as sa
from h.db import Base
from sqlalchemy.orm import exc
from sqlalchemy import and_


class Translation(Base):
    """
    Represents a translation in the database
    """
    __tablename__ = 'translation'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    page_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.pages.models.Page.id))
    page = sa.orm.relationship('Page', backref='page_translation')

    language_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.languages.models.Language.id))
    language = sa.orm.relationship('Language', backref='language_translation')

    group_id = sa.Column(sa.Integer, sa.ForeignKey(h.groups.models.Group.id))
    group = sa.orm.relationship('Group', backref='group_translation')

    def __init__(self, page, language, group):
        """
        Initializes a translation
        :param page: the page
        :param language: the language
        :param group: the group
        """
        if group and page and language:
            self.page_id = page.id
            self.language_id = language.id
            self.group_id = group.id

    @classmethod
    def get_translation(cls, page, language, group):
        """
        Retrieve a translation by page, language and group
        :param page: the page ID
        :param language: the language ID
        :param group: the group ID
        :return: a translation or None
        """
        try:
            if group is None:
                return cls.query.filter(
                    cls.page_id == page.id,
                    cls.language_id == language.id,
                    cls.group_id == -1).one()
            else:
                return cls.query.filter(
                    cls.page_id == page.id,
                    cls.language_id == language.id,
                    cls.group_id == group.id).one()
        except exc.NoResultFound:
            return None


    @classmethod
    def get_public_translations(cls, page):
        """
        Get a list of public translations for a page
        :param page: the page to query
        :return: a list of languages or an empty list
        """
        try:
            return lang_models.Language.query.\
                join(cls, and_(cls.page_id == page.id,
                               cls.group_id == -1,
                               lang_models.Language.id == cls.language_id)).\
                with_entities(lang_models.Language.id,
                              lang_models.Language.name,
                              lang_models.Language.pubid,
                              cls.group_id).all()
        except exc.NoResultFound:
            return None

    @classmethod
    def get_page_translations(cls, page):
        """
        Get a list of public translations for a page
        :param page: the page to query
        :return: a list of languages or an empty list
        """
        try:
            return lang_models.Language.query.\
                join(cls, and_(cls.page_id == page.id,
                               lang_models.Language.id == cls.language_id)).\
                with_entities(lang_models.Language.id,
                              lang_models.Language.name,
                              lang_models.Language.pubid,
                              cls.group_id).all()
        except exc.NoResultFound:
            return None

    '''
        We currently do not support deletion of added translation.
        This means once language is added for a page and a group, it will be there for all
        authorised users even without any translations on the page.
        The only way to remove such "empty" translations is for admin to directly remove them from the database.
    '''
    @classmethod
    def delete_translation(cls, page, language, group):
        """
        Delete all translation for a page, language and group
        :param page: the page ID
        :param language: the language ID
        :param group: the group ID
        :return: the result of the delete method or None
        """
        return None

    @classmethod
    def get_by_id(cls, id_):
        """
        Get a vote by ID
        :param id_: the ID to query
        :return: a vote or None
        """
        try:
            return cls.query.filter(
                cls.id == id_).one()
        except exc.NoResultFound:
            return None

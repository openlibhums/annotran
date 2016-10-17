# -*- coding: utf-8 -*-


import annotran
import annotran.languages.models
import annotran.pages.models
import h
import h.accounts.models
import h.groups.models
import sqlalchemy as sa
from h.db import Base
from sqlalchemy import and_
from sqlalchemy.orm import exc


class Vote(Base):
    """
    Represents a vote in the database
    """
    __tablename__ = 'vote'

    score = sa.Column(sa.Integer,
                      nullable=False)

    page_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.pages.models.Page.id), primary_key=True)
    page = sa.orm.relationship('Page', backref='page_vote')

    language_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.languages.models.Language.id), primary_key=True)
    language = sa.orm.relationship('Language', backref='language_vote')

    group_id = sa.Column(sa.Integer, sa.ForeignKey(h.groups.models.Group.id), primary_key=True)
    group = sa.orm.relationship('Group', backref='group_vote')

    author_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id), primary_key=True)
    author = sa.orm.relationship('User', backref='author_vote', foreign_keys=[author_id])

    voter_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id), primary_key=True)
    voter = sa.orm.relationship('User', backref='voter_vote', foreign_keys=[voter_id])

    def __init__(self, score, page, language, group, author, voter):
        """
        Initializes a vote
        :param score: the score
        :param page: the page
        :param language: the language
        :param group: the group
        :param author: the author
        :param voter: the voter
        """
        if score and page and language and author and voter:
            self.score = score
            self.page_id = page.id
            self.language_id = language.id

            if group is not None:
                self.group_id = group.id
            self.author_id = author.id
            self.voter_id = voter.id

    @classmethod
    def get_vote(cls, page, language, group, author, voter):
        """
        Retrieve a vote by page, language, group, author and voter
        :param page: the page ID
        :param language: the language ID
        :param group: the group ID
        :param author: the author ID
        :param voter: the voter ID
        :return: a vote or None
        """
        try:
            if group is None:
                return cls.query.filter(
                    cls.page_id == page.id,
                    cls.language_id == language.id,
                    cls.group_id == -1,
                    cls.author_id == author.id,
                    cls.voter_id == voter.id).one()
            else:
                return cls.query.filter(
                    cls.page_id == page.id,
                    cls.language_id == language.id,
                    cls.group_id == group.id,
                    cls.author_id == author.id,
                    cls.voter_id == voter.id).one()
        except exc.NoResultFound:
            return None

    # returns avg of author scores per page, language, and group
    @classmethod
    def get_author_scores(cls, page, language, group=None):
        """
        Retrieve the average author scores for a page, language and group
        :param page: the page ID
        :param language: the language ID
        :param group: the group ID
        :return: an average of the scores
        """
        if page and language and not group:
            try:
                return \
                    h.accounts.models.User.query.join(cls,
                                                      and_(cls.page_id == page.id,
                                                           cls.language_id == language.id,
                                                           cls.group_id == -1,
                                                           h.accounts.models.User.id == cls.author_id)).with_entities(
                        h.accounts.models.User.username,
                        sa.func.avg(cls.score).label('average')).group_by(h.accounts.models.User.username).order_by(
                        sa.func.avg(cls.score).desc()).all()
            except exc.NoResultFound:
                return None

        elif page and language:
            try:
                return \
                    h.accounts.models.User.query.join(cls,
                                                      and_(cls.page_id == page.id,
                                                           cls.language_id == language.id,
                                                           cls.group_id == group.id,
                                                           h.accounts.models.User.id == cls.author_id)).with_entities(
                        h.accounts.models.User.username,
                        sa.func.avg(cls.score).label('average')).group_by(h.accounts.models.User.username).order_by(
                        sa.func.avg(cls.score).desc()).all()
            except exc.NoResultFound:
                return None
        else:
            return None

    @classmethod
    def delete_votes(cls, page, language, group, author):
        """
        Delete all votes for a page, language, group and author
        :param page: the page ID
        :param language: the language ID
        :param group: the group ID
        :param author: the author ID
        :return: the result of the delete method or None
        """
        try:
            if group is None:
                return cls.query.filter(
                    cls.page_id == page.id,
                    cls.language_id == language.id,
                    cls.group_id == -1,
                    cls.author_id == author.id).delete()
            else:
                return cls.query.filter(
                    cls.page_id == page.id,
                    cls.language_id == language.id,
                    cls.group_id == group.id,
                    cls.author_id == author.id).delete()
        except exc.NoResultFound:
            return None

    @classmethod
    def get_by_id(cls, vote):
        """
        Get a vote by ID
        :param id_: the ID to query
        :return: a vote or None
        """
        try:
            return cls.query.filter(
                cls.page_id == vote.page_id,
                cls.language_id == vote.language_id,
                cls.group_id == vote.group_id,
                cls.author_id == vote.author_id,
                cls.voter_id == vote.voter_id).one()
        except exc.NoResultFound:
            return None

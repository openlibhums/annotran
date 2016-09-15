# -*- coding: utf-8 -*-


import h

from sqlalchemy.orm import exc
from h.db import Base
import sqlalchemy as sa
import annotran
from sqlalchemy import *



class Vote(Base):
    __tablename__ = 'vote'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    score = sa.Column(sa.Integer,
                      nullable=False)

    page_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.pages.models.Page.id))
    page = sa.orm.relationship('Page', backref='pvote')

    language_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.languages.models.Language.id))
    language = sa.orm.relationship('Language', backref='lvote')

    group_id = sa.Column(sa.Integer, sa.ForeignKey(h.groups.models.Group.id), nullable=True)
    group = sa.orm.relationship('Group', backref='gvote')

    author_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id))
    author = sa.orm.relationship('User', backref='avote', foreign_keys=[author_id])

    voter_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id))
    voter = sa.orm.relationship('User', backref='vvote', foreign_keys=[voter_id])

    def __init__(self, score, page, language, group, author, voter):
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

    #returns avg of author scores per page, language, and group
    @classmethod
    def get_author_scores_plg(cls, page, language, group=None):
        if page and language and not group:
            try:
                return\
                    h.accounts.models.User.query.join(cls,
                                                  and_(cls.page_id == page.id,
                                                       cls.language_id == language.id,
                                                       cls.group_id == -1,
                                                       h.accounts.models.User.id == cls.author_id)).\
                    with_entities(h.accounts.models.User.username,
                                  sa.func.avg(cls.score).label('average')).\
                        group_by(h.accounts.models.User.username).\
                        order_by(sa.func.avg(cls.score).desc()).\
                        all()
            except exc.NoResultFound:
                return None

        elif page and language:
            try:
                return\
                    h.accounts.models.User.query.join(cls,
                                                  and_(cls.page_id == page.id,
                                                       cls.language_id == language.id,
                                                       cls.group_id == group.id,
                                                       h.accounts.models.User.id == cls.author_id)).\
                    with_entities(h.accounts.models.User.username,
                                  sa.func.avg(cls.score).label('average')).\
                        group_by(h.accounts.models.User.username).\
                        order_by(sa.func.avg(cls.score).desc()).all()
            except exc.NoResultFound:
                return None
        else:
            return None

    @classmethod
    def delete_votes(cls, page, language, group, author):
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
    def get_by_id(cls, id_):
        """Return the vote with the given id, or None."""
        try:
            return cls.query.filter(
                cls.id == id_).one()
        except exc.NoResultFound:
            return None

    @classmethod
    def get_by_vote(cls, vote):
        """Return the vote with the given vote value, or None."""
        try:
            return cls.query.filter(
                cls.vote == vote).one()
        except exc.NoResultFound:
            return None
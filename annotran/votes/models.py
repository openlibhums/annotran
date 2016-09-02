# -*- coding: utf-8 -*-

import sqlalchemy as sa
import h

from sqlalchemy.orm import exc
from h.db import Base
#from sqlalchemy.sql import func
import sqlalchemy as sa
import annotran



class Vote(Base):
    __tablename__ = 'vote'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    score = sa.Column(sa.Integer,
                      nullable=False)

    page_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.pages.models.Page.id))
    page = sa.orm.relationship('Page', backref='pvote')

    language_id = sa.Column(sa.Integer, sa.ForeignKey(annotran.languages.models.Language.id))
    language = sa.orm.relationship('Language', backref='lvote')

    group_id = sa.Column(sa.Integer, sa.ForeignKey(h.groups.models.Group.id))
    group = sa.orm.relationship('Group', backref='gvote')

    author_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id))
    author = sa.orm.relationship('User', backref='avote', foreign_keys=[author_id])

    voter_id = sa.Column(sa.Integer, sa.ForeignKey(h.accounts.models.User.id))
    voter = sa.orm.relationship('User', backref='vvote', foreign_keys=[voter_id])

    def __init__(self, score, page, language, group, author, voter):
        if score and page and language and group and author and voter:
            self.score = score
            self.page_id = page.id
            self.language_id = language.id
            self.group_id = group.id
            self.author_id = author.id
            self.voter_id = voter.id

    @classmethod
    def get_vote(cls, page, language, group, author, voter):
        try:
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
    def get_author_scores_plg(cls, page, language, group):
        if page and language and group:
            try:
                return cls.query.filter(
                    cls.page_id == page.id,
                    cls.language_id == language.id,
                    cls.group_id == group.id).\
                    with_entities(cls.author_id,
                                  sa.func.avg(cls.score).label('average'))\
                    .group_by(cls.author_id).all()



                '''
                query1 = cls.query.filter(
                    cls.page_id == page.id, cls.language_id == language.id, cls.group_id == group.id,
                    cls.vote_type_id == type).with_entities(cls.id, annotran.pages.models.VoteValue.value)

                query2 = cls.query.filter(
                    cls.page_id == page.id, cls.language_id == language.id, cls.group_id == group.id,
                    cls.vote_type_id == type).with_entities(cls.id, cls.user_id,
                    sa.func.avg(annotran.pages.models.VoteValue.value).label('average'))\
                    .group_by(cls.id).all()





                    .filter(annotran.pages.models.VoteValue.members.contains(cls.id))\
                    .with_entities(cls.user_id, sa.func.avg(annotran.pages.models.VoteValue.value).label('average'))\
                    .group_by(cls.user_id).all()
                '''

            except exc.NoResultFound:
                return None
        else:
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

    '''
    @classmethod
    def get_votes_for_authors(cls, page, language):
        """Return avg votes per author on page for selected language, or None"""
        h.accounts.models.User.query.filter(cls.relPage.contains(page), cls.relLanguage.contains(language), cls.relUser)\
            .with_entities(h.accounts.models.User.username, sa.func.avg(cls.vote).label('average'))\
            .group_by(h.accounts.models.User.username).all()
        return None
    '''

    @classmethod
    def get_by_language(cls, language):
        """Return the language with the given pubid, or None."""
        '''
        if language:
            return cls.query.filter(cls.relLanguage.contains(language))
        else:
            return None
        '''
        return None
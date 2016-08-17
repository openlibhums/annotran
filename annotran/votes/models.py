import datetime

import sqlalchemy as sa
from sqlalchemy.orm import exc

from h.db import Base


class Vote(Base):
    __tablename__ = 'vote'

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    vote = sa.Column(sa.Text(),
                      unique=True,
                      nullable=False)
    # we need a relationship table between a vote and: a user, a langauge and a page
    relUser = sa.orm.relationship('User',
                                  backref='votes',
                                  secondary='user_vote')

    relVoter = sa.orm.relationship('User',
                                  backref='voters',
                                  secondary='voter_vote')

    relLanguage = sa.orm.relationship('Language',
                                  backref='votes',
                                  secondary='language_vote')

    relPage = sa.orm.relationship('Page',
                                  backref='votes',
                                  secondary='page_vote')

    def __init__(self, vote, user = None, language=None, page = None):
        self.vote = vote
        if user and language and page:
            self.relUser.append(user)
            self.relLanguage.append(language)
            self.relPage.append(page)

    @classmethod
    def get_by_vote(cls, vote):
        """Return the vote with the given vote value, or None."""
        try:
            return cls.query.filter(
                cls.vote == vote).one()
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

USER_VOTE_TABLE = sa.Table(
    'user_vote', Base.metadata,
    sa.Column('user_id',
              sa.Integer,
              sa.ForeignKey('user.id'),
              nullable=False),
    sa.Column('vote_id',
              sa.Integer,
              sa.ForeignKey('vote.id'),
              nullable=False)
)

VOTER_VOTE_TABLE = sa.Table(
    'voter_vote', Base.metadata,
    sa.Column('user_id',
              sa.Integer,
              sa.ForeignKey('user.id'),
              nullable=False),
    sa.Column('vote_id',
              sa.Integer,
              sa.ForeignKey('vote.id'),
              nullable=False)
)

LANGUAGE_VOTE_TABLE = sa.Table(
    'language_vote', Base.metadata,
    sa.Column('language_id',
              sa.Integer,
              sa.ForeignKey('language.id'),
              nullable=False),
    sa.Column('vote_id',
              sa.Integer,
              sa.ForeignKey('vote.id'),
              nullable=False)
)

PAGE_VOTE_TABLE = sa.Table(
    'page_vote', Base.metadata,
    sa.Column('page_id',
              sa.Integer,
              sa.ForeignKey('page.id'),
              nullable=False),
    sa.Column('vote_id',
              sa.Integer,
              sa.ForeignKey('vote.id'),
              nullable=False)
)

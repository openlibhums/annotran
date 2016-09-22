# -*- coding: utf-8 -*-

from h import db
from h.test import factories
from h.groups import models as groups_models
from annotran.languages import models as lang_models
from annotran.pages import models as pages_models
from annotran.votes import models as votes_models


def test_init():
    score = 5
    author = factories.User()
    voter = factories.User()

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    v = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(v)

    db.Session.flush()

    assert v.id
    assert v.score == score
    assert v.page_id == p.id
    assert v.language_id == l.id
    assert v.group_id == g.id
    assert v.author_id == author.id
    assert v.voter_id == voter.id

def test_get_vote():
    score = 5
    author = factories.User()
    voter = factories.User()

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    v = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(v)

    db.Session.flush()

    assert votes_models.Vote.get_vote(p, l, g, author, voter) == score

def test_get_author_scores_plg_when_group_none():
    score = 5
    author = factories.User()
    voter = factories.User()

    g = None

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    v = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(v)

    db.Session.flush()

    assert votes_models.Vote.get_author_scores(p, l) == v

def test_get_author_scores_plg_when_group_not_none():
    score = 5
    author = factories.User()
    voter = factories.User()

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    v = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(v)

    db.Session.flush()

    assert votes_models.Vote.get_author_scores(p, l, g) == v


def test_get_by_id_when_id_does_exist():
    score = 5
    author = factories.User()
    voter = factories.User()

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    v = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(v)

    db.Session.flush()

    assert votes_models.Vote.get_by_id(v.id) == v

def test_get_by_id_when_id_does_not_exist():
    score = 5
    author = factories.User()
    voter = factories.User()

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    v = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(v)

    db.Session.flush()

    assert votes_models.Vote.get_by_id(25) is None






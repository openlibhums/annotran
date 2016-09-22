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
    db.Session.add(author)
    db.Session.add(voter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    vote = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(vote)
    db.Session.flush()

    assert vote.id
    assert vote.score == score
    assert vote.page_id == p.id
    assert vote.language_id == l.id
    assert vote.group_id == g.id
    assert vote.author_id == author.id
    assert vote.voter_id == voter.id

def test_get_vote():
    score = 5
    author = factories.User()
    voter = factories.User()
    db.Session.add(author)
    db.Session.add(voter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    vote = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(vote)

    db.Session.flush()

    assert votes_models.Vote.get_vote(p, l, g, author, voter) == vote


def test_get_author_scores_group_none_single_voter_author():
    score = 5
    author = factories.User()
    voter = factories.User()
    db.Session.add(author)
    db.Session.add(voter)

    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    #vote for a group None
    vote = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(vote)

    db.Session.flush()

    assert votes_models.Vote.get_author_scores(p, l)[0][1] == score


def test_get_author_scores_group_none_single_author_multiple_voters():
    ##add record 1
    score1 = 5
    author = factories.User()
    voter1 = factories.User()
    db.Session.add(author)
    db.Session.add(voter1)

    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    #add record 2
    score2 = 3
    voter2 = factories.User()
    db.Session.add(voter2)

    #vote for a group None
    vote1 = votes_models.Vote(score1, p, l, g, author, voter1)
    db.Session.add(vote1)
    db.Session.flush()

    vote2 = votes_models.Vote(score2, p, l, g, author, voter2)
    db.Session.add(vote2)
    db.Session.flush()

    #testing average score for a single author with two votes
    assert votes_models.Vote.get_author_scores(p, l)[0][1] == ((score1+score2)/2)


def test_get_author_scores_group_none_multiple_authors_voters():
    score_a_1_v_1 = 5
    score_a_1_v_2 = 3

    score_a_2_v_1 = 4
    score_a_2_v_2 = 2

    author1 = factories.User()
    voter1 = factories.User()
    db.Session.add(author1)
    db.Session.add(voter1)

    author2 = factories.User()
    voter2 = factories.User()
    db.Session.add(author2)
    db.Session.add(voter2)

    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    #votes: author_1, voter_1, voter_2
    vote_a_1_v_1 = votes_models.Vote(score_a_1_v_1, p, l, g, author1, voter1)
    db.Session.add(vote_a_1_v_1)
    db.Session.flush()

    vote_a_1_v_2 = votes_models.Vote(score_a_1_v_2, p, l, g, author1, voter2)
    db.Session.add(vote_a_1_v_2)
    db.Session.flush()

    #votes: author_2, voter_1, voter_2
    vote_a_2_v_1 = votes_models.Vote(score_a_2_v_1, p, l, g, author2, voter1)
    db.Session.add(vote_a_2_v_1)
    db.Session.flush()

    vote_a_2_v_2 = votes_models.Vote(score_a_2_v_2, p, l, g, author2, voter2)
    db.Session.add(vote_a_2_v_2)
    db.Session.flush()


    print votes_models.Vote.get_author_scores(p, l)

    #testing average scores
    assert votes_models.Vote.get_author_scores(p, l)[0][1] == ((score_a_1_v_1+score_a_1_v_2)/2)
    assert votes_models.Vote.get_author_scores(p, l)[1][1] == ((score_a_2_v_1+score_a_2_v_2)/2)

def test_get_author_scores_group_not_none_single_voter_author():
    score = 5
    author = factories.User()
    voter = factories.User()
    db.Session.add(author)
    db.Session.add(voter)

    g = groups_models.Group(name="abc_group", creator=author)
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    #vote for a group None
    vote = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(vote)

    db.Session.flush()

    assert votes_models.Vote.get_author_scores(p, l, g)[0][1] == score

def test_get_author_scores_group_not_none_single_author_multiple_voters():
    ##add record 1
    score1 = 5
    author = factories.User()
    voter1 = factories.User()
    db.Session.add(author)
    db.Session.add(voter1)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    #add record 2
    score2 = 3
    voter2 = factories.User()
    db.Session.add(voter2)

    #vote for a group None
    vote1 = votes_models.Vote(score1, p, l, g, author, voter1)
    db.Session.add(vote1)
    db.Session.flush()

    vote2 = votes_models.Vote(score2, p, l, g, author, voter2)
    db.Session.add(vote2)
    db.Session.flush()

    #testing average score for a single author with two votes
    assert votes_models.Vote.get_author_scores(p, l, g)[0][1] == ((score1+score2)/2)


def test_get_author_scores_group_not_none_multiple_authors_voters():
    score_a_1_v_1 = 5
    score_a_1_v_2 = 3

    score_a_2_v_1 = 4
    score_a_2_v_2 = 2

    author1 = factories.User()
    voter1 = factories.User()
    db.Session.add(author1)
    db.Session.add(voter1)

    author2 = factories.User()
    voter2 = factories.User()
    db.Session.add(author2)
    db.Session.add(voter2)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    #votes: author_1, voter_1, voter_2
    vote_a_1_v_1 = votes_models.Vote(score_a_1_v_1, p, l, g, author1, voter1)
    db.Session.add(vote_a_1_v_1)
    db.Session.flush()

    vote_a_1_v_2 = votes_models.Vote(score_a_1_v_2, p, l, g, author1, voter2)
    db.Session.add(vote_a_1_v_2)
    db.Session.flush()

    #votes: author_2, voter_1, voter_2
    vote_a_2_v_1 = votes_models.Vote(score_a_2_v_1, p, l, g, author2, voter1)
    db.Session.add(vote_a_2_v_1)
    db.Session.flush()

    vote_a_2_v_2 = votes_models.Vote(score_a_2_v_2, p, l, g, author2, voter2)
    db.Session.add(vote_a_2_v_2)
    db.Session.flush()

    #testing average scores
    assert votes_models.Vote.get_author_scores(p, l, g)[0][1] == ((score_a_1_v_1+score_a_1_v_2)/2)
    assert votes_models.Vote.get_author_scores(p, l, g)[1][1] == ((score_a_2_v_1+score_a_2_v_2)/2)

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
    db.Session.flush()

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
    db.Session.flush()

    v = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(v)

    db.Session.flush()

    assert votes_models.Vote.get_by_id(25) is None

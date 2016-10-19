# -*- coding: utf-8 -*-

from h import db
from h.test import factories
from h.groups import models as groups_models
from annotran.languages import models as lang_models
from annotran.pages import models as pages_models
from annotran.votes import models as votes_models

def test_init():
    """
        This should add a vote to a database session for a given author, voter, group, language, and page.
    """
    score = 5
    author = factories.User()
    voter = factories.User()
    db.Session.add(author)
    db.Session.add(voter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    vote = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(vote)
    db.Session.flush()

    assert vote.score == score
    assert vote.page_id == p.id
    assert vote.language_id == l.id
    assert vote.group_id == g.id
    assert vote.author_id == author.id
    assert vote.voter_id == voter.id

def test_get_vote():
    """
        This should get a vote for a given author, voter, group, language, and page.
    """
    score = 5
    author = factories.User()
    voter = factories.User()
    db.Session.add(author)
    db.Session.add(voter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    vote = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(vote)

    db.Session.flush()

    assert votes_models.Vote.get_vote(p, l, g, author, voter) == vote

def test_get_vote_input_val_none():
    """
        This should return None, and do not throw an exception.
    """
    assert votes_models.Vote.get_vote(None, None, None, None, None) == None

def test_get_author_scores_public_group_single_voter_author():
    """
        Method get_author_scores returns avg scores for all authors with translations for a given page, language and group.
        This test should return the value of a single score for a single author
        with translations for a given page and language and for a public group,
    """
    score = 5
    author = factories.User()
    voter = factories.User()
    db.Session.add(author)
    db.Session.add(voter)

    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    #vote for a public group
    vote = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(vote)

    db.Session.flush()

    assert votes_models.Vote.get_author_scores(p, l)[0][1] == score

def test_get_author_scores_public_group_single_author_multiple_voters():
    """
        Method get_author_scores returns avg scores for all authors with translations for a given page, language and group.
        This test should return the avg of two scores for a single author
        with translations for a given page and language an for a public group,
    """
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

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    #add record 2
    score2 = 3
    voter2 = factories.User()
    db.Session.add(voter2)

    #vote for a public group
    vote1 = votes_models.Vote(score1, p, l, g, author, voter1)
    db.Session.add(vote1)
    db.Session.flush()

    vote2 = votes_models.Vote(score2, p, l, g, author, voter2)
    db.Session.add(vote2)
    db.Session.flush()

    #testing average score for a single author with two votes
    assert votes_models.Vote.get_author_scores(p, l)[0][1] == ((score1+score2)/2)

def test_get_author_scores_private_group_single_voter_author():
    """
        Method get_author_scores returns avg scores for all authors with translations for a given page, language and group.
        This test should return the value of a single score for a single author
        with translations for a given page and language and for a private group,
    """
    score = 5
    author = factories.User()
    voter = factories.User()
    db.Session.add(author)
    db.Session.add(voter)

    g = groups_models.Group(name="test_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    #vote for a public group
    vote = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(vote)

    db.Session.flush()

    assert votes_models.Vote.get_author_scores(p, l, g)[0][1] == score

def test_get_author_scores_private_group_single_author_multiple_voters():
    """
        Method get_author_scores returns avg scores for all authors with translations for a given page, language and group.
        This test should return the avg of two scores for a single author
        with translations for a given page and language an for a private group,
    """
    ##add record 1
    score1 = 5
    author = factories.User()
    voter1 = factories.User()
    db.Session.add(author)
    db.Session.add(voter1)

    g = groups_models.Group(name="test_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    #add record 2
    score2 = 3
    voter2 = factories.User()
    db.Session.add(voter2)

    #vote for a public group
    vote1 = votes_models.Vote(score1, p, l, g, author, voter1)
    db.Session.add(vote1)
    db.Session.flush()

    vote2 = votes_models.Vote(score2, p, l, g, author, voter2)
    db.Session.add(vote2)
    db.Session.flush()

    #testing average score for a single author with two votes
    assert votes_models.Vote.get_author_scores(p, l, g)[0][1] == ((score1+score2)/2)

def test_get_author_scores_input_val_none():
    """
        This should return None, and do not throw an exception.
    """
    assert votes_models.Vote.get_author_scores(None, None) == None

def test_get_author_scores_public_group_multiple_authors_voters():
    """
        This test should return the avg of two scores for two authors
        with translations for a given page and language an for a public group,
    """
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

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
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
    assert votes_models.Vote.get_author_scores(p, l)[0][1] == ((score_a_1_v_1+score_a_1_v_2)/2)
    assert votes_models.Vote.get_author_scores(p, l)[1][1] == ((score_a_2_v_1+score_a_2_v_2)/2)

def test_get_author_scores_private_group_multiple_authors_voters():
    """
        This test should return the avg of two scores for two authors
        with translations for a given page and language an for a private group,
    """
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

    g = groups_models.Group(name="test_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
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
    """
        This should return a vote for a given composite id: page_id, language_id, group_id, author_id, voter_id.
    """
    score = 5
    author = factories.User()
    voter = factories.User()
    db.Session.add(author)
    db.Session.add(voter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    vote = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(vote)
    db.Session.flush()

    assert votes_models.Vote.get_by_id(p.id, l.id, g.id, author.id, voter.id) == vote

def test_get_by_id_when_id_does_not_exist():
    """
        This should None for a composite id that does not exist in a db.
    """
    assert votes_models.Vote.get_by_id(25, 26, 27, 28, 29) is None

def test_delete_votes_public_group_single_voter_author():
    """
        This test should add a score for a single author with translations for
        a given page and language and for a public group, Then, it should delete
        the record and as a result return an empty array.
    """
    score = 5
    author = factories.User()
    voter = factories.User()
    db.Session.add(author)
    db.Session.add(voter)

    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    #vote for a public group
    vote = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(vote)

    db.Session.flush()

    assert votes_models.Vote.get_author_scores(p, l)[0][1] == score

    votes_models.Vote.delete_votes(p, l, g, author)

    assert votes_models.Vote.get_author_scores(p, l) == []

def test_delete_votes_private_group_single_voter_author():
    """
        This test should add a score for a single author with translations for
        a given page and language and for a private group, Then, it should delete
        the record and as a result return an empty array.
    """
    score = 5
    author = factories.User()
    voter = factories.User()
    db.Session.add(author)
    db.Session.add(voter)

    g = groups_models.Group(name="test-group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    #vote for a public group
    vote = votes_models.Vote(score, p, l, g, author, voter)
    db.Session.add(vote)

    db.Session.flush()

    assert votes_models.Vote.get_author_scores(p, l, g)[0][1] == score

    votes_models.Vote.delete_votes(p, l, g, author)

    assert votes_models.Vote.get_author_scores(p, l, g) == []

def test_delete_votes_public_group_multiple_authors_voters():
    """
        This test should add scores for two authors with translations for
        a given page and language and for a public group, Then, it should delete all
        records and as a result return an empty array.
    """
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

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
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
    assert votes_models.Vote.get_author_scores(p, l)[0][1] == ((score_a_1_v_1+score_a_1_v_2)/2)
    assert votes_models.Vote.get_author_scores(p, l)[1][1] == ((score_a_2_v_1+score_a_2_v_2)/2)

    votes_models.Vote.delete_votes(p, l, g, author1)
    votes_models.Vote.delete_votes(p, l, g, author2)

    assert votes_models.Vote.get_author_scores(p, l) == []

def test_delete_votes_private_group_multiple_authors_voters():
    """
        This test should add scores for two authors with translations for
        a given page and language and for a public group, Then, it should delete all
        records and as a result return an empty array.
    """
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

    g = groups_models.Group(name="test-group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
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

    votes_models.Vote.delete_votes(p, l, g, author1)
    votes_models.Vote.delete_votes(p, l, g, author2)

    assert votes_models.Vote.get_author_scores(p, l, g) == []
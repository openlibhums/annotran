# -*- coding: utf-8 -*-
import mock
import pytest
from pyramid import httpexceptions


from annotran.votes import views



_SENTINEL = object()


def _mock_request(feature=None, settings=None, params=None,
                  authenticated_userid=_SENTINEL, route_url=None, **kwargs):
    """Return a mock Pyramid request object."""
    params = params or {"foo": "bar"}
    if authenticated_userid is _SENTINEL:
        authenticated_userid = "acct:fred@hypothes.is"
    return mock.Mock(
        feature=feature or (lambda feature: True),
        registry=mock.Mock(settings=settings or {}),
        params=params, POST=params,
        authenticated_userid=authenticated_userid,
        route_url=route_url or mock.Mock(return_value="test-read-url"),
        **kwargs)

# The fixtures required to mock all of create()'s dependencies.
create_fixtures = pytest.mark.usefixtures('Vote',
                                          'session_model')


@create_fixtures
def test_create_adds_vote_to_db(Vote, Group, Language, Page, User):
    """This should add the new vote to the database session."""
    author = mock.Mock(id=1, username="test", uid="test")
    User.return_value = author

    vote = mock.Mock(id=1)
    Vote.return_value = vote

    group = mock.Mock(id=1)
    Group.return_value = group

    page = mock.Mock(id=1, uri='http://www.annotran_test.com')
    Page.return_value = page

    language = mock.Mock(id=1)
    Language.return_value = language

    request = _mock_request(matchdict={'page_uri': page.uri,
                                       'public_group_id': group.pubid,
                                       'public_language_id': language.pubid,
                                       'score': 5,
                                       'username': author.username},
                            authenticated_user=mock.Mock(id=2, username="test2", uid="test2"))

    views.add_vote(request)

    #request.db.add.assert_called_once_with()


@create_fixtures
def test_create_redirects_to_vote_read_vote(Vote, Group, Language, Page, User):
    """After successfully creating a new vote it should redirect."""
    author = mock.Mock(id=1, username="test", uid="test")
    User.return_value = author

    vote = mock.Mock(id=1)
    Vote.return_value = vote

    group = mock.Mock(id=1)
    Group.return_value = group

    page = mock.Mock(id=1, uri='http://www.annotran_test.com')
    Page.return_value = page

    language = mock.Mock(id=1)
    Language.return_value = language

    request = _mock_request(matchdict={'page_uri': page.uri,
                                       'public_group_id': group.pubid,
                                       'public_language_id': language.pubid,
                                       'score': 5,
                                       'username': author.username},
                            authenticated_user=mock.Mock(id=2, username="test2", uid="test2"))

    result = views.add_vote(request)

    assert isinstance(result, httpexceptions.HTTPRedirection)

@pytest.fixture
def Vote(request):
    patcher = mock.patch('annotran.votes.models.Vote', autospec=True)
    request.addfinalizer(patcher.stop)
    return patcher.start()

@pytest.fixture
def Page(request):
    patcher = mock.patch('annotran.pages.models.Page', autospec=True)
    request.addfinalizer(patcher.stop)
    return patcher.start()

@pytest.fixture
def Language(request):
    patcher = mock.patch('annotran.languages.models.Language', autospec=True)
    request.addfinalizer(patcher.stop)
    return patcher.start()

@pytest.fixture
def Group(request):
    patcher = mock.patch('h.groups.models.Group', autospec=True)
    request.addfinalizer(patcher.stop)
    return patcher.start()

@pytest.fixture
def User(request):
    patcher = mock.patch('h.accounts.models.User', autospec=True)
    request.addfinalizer(patcher.stop)
    return patcher.start()

@pytest.fixture
def session_model(request):
    patcher = mock.patch('annotran.session.model')
    request.addfinalizer(patcher.stop)
    return patcher.start()




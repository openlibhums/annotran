# -*- coding: utf-8 -*-
import mock
import pytest
from pyramid import httpexceptions as exc

from annotran.reports import views
from annotran.admin import *

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
create_fixtures = pytest.mark.usefixtures('Report',
                                          'session_model')


@create_fixtures
def test_create_adds_new_report_to_db(Group, Language, Page, User):
    """This should add the new report to the database session."""
    author = mock.Mock(id=1, username="test", uid="test")
    User.return_value = author

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
                                       'user_id': author.username},
                            authenticated_user=mock.Mock(id=2, username="test2", uid="test2"))

    delete_report(page, language, group, author)
    assert views.add_report(request).status_code == 200


@create_fixtures
def test_create_adds__existing_report_to_db(Report, Group, Language, Page, User):
    author = mock.Mock(id=1, username="test", uid="test")
    User.return_value = author

    report = mock.Mock(id=1)
    Report.return_value = report

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
                                       'user_id': author.username},
                            authenticated_user=mock.Mock(id=2, username="test2", uid="test2"))

    delete_report(page, language, group, author)

    assert views.add_report(request).status_code == 400


'''
@create_fixtures
def test_create_redirects_to_report_read_report(Report, Group, Language, Page, User):
    """After successfully creating a new report it should redirect."""
    author = mock.Mock(id=1, username="test", uid="test")
    User.return_value = author

    report = mock.Mock(id=1)
    Report.return_value = report

    group = mock.Mock(id=1)
    Group.return_value = group

    page = mock.Mock(id=1, uri='http://www.annotran_test.com')
    Page.return_value = page

    language = mock.Mock(id=1)
    Language.return_value = language

    request = _mock_request(matchdict={'page_id': page.uri,
                                       'public_group_id': group.pubid,
                                       'public_language_id': language.pubid,
                                       'score': 5,
                                       'username': author.username},
                            authenticated_user=mock.Mock(id=2, username="test2", uid="test2"))

    result = views.add_report(request)

    assert isinstance(result, httpexceptions.HTTPRedirection)
'''


@pytest.fixture
def Report(request):
    patcher = mock.patch('annotran.reports.models.Report', autospec=True)
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




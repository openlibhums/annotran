# -*- coding: utf-8 -*-
import mock
import pytest
from pyramid import httpexceptions

from annotran.pages import models as page_model
from h.test import factories
from annotran.pages import views



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
create_fixtures = pytest.mark.usefixtures('Page',
                                          'session_model')

@create_fixtures
def test_create_adds_page_to_db(Page, Group, Language):
    """This should add the new page to the database session."""
    page = mock.Mock(uri='http://www.annotran_testing8.com')
    Page.return_value = page

    group = mock.Mock(id=1)
    Group.return_value = group

    language = mock.Mock(id=1)
    Language.return_value = language

    request = _mock_request(matchdict={'language_name': 'test_language', 'public_group_id': group.pubid, 'page_url': 'http://www.annotran_testing8.com'})

    views.add_page(request)

    #request.db.add.assert_called_once_with()


@create_fixtures
def test_create_redirects_to_page_read_page(Page, Group, Language):
    """After successfully creating a new page it should redirect."""
    page = mock.Mock(id=1)
    Page.return_value = page

    group = mock.Mock(id=1)
    Group.return_value = group

    language = mock.Mock(id=1)
    Language.return_value = language

    request = _mock_request(matchdict={'language_name': 'test_language', 'public_group_id':
        group.pubid, 'page_url': 'http://www.annotran_test.com'})


    result = views.add_page(request)

    assert isinstance(result, httpexceptions.HTTPRedirection)

@create_fixtures
def test_create_with_non_ascii_name(Group, Language):
    group = mock.Mock(id=1)
    Group.return_value = group

    language = mock.Mock(id=1)
    Language.return_value = language

    views.add_page(_mock_request(matchdict={'public_group_id': group.pubid, 'language_name': u"☆ ßüper Gröup ☆",
                                            'page_url': 'http://www.annotran_test.com'}))

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
def session_model(request):
    patcher = mock.patch('annotran.session.model')
    request.addfinalizer(patcher.stop)
    return patcher.start()




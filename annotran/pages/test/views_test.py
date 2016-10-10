# -*- coding: utf-8 -*-
import mock
import pytest
from pyramid import httpexceptions

from annotran.pages import views


_SENTINEL = object()


def _mock_request(feature=None, settings=None, params=None,
                  authenticated_userid=_SENTINEL, route_url=None, **kwargs):
    """Return a mock Pyramid request object."""
    params = params or {"foo": "bar"}
    if authenticated_userid is _SENTINEL:
        authenticated_userid = "acct:fred@annotran.com"
    return mock.Mock(
        feature=feature or (lambda feature: True),
        registry=mock.Mock(settings=settings or {}),
        params=params, POST=params,
        authenticated_userid=authenticated_userid,
        route_url=route_url or mock.Mock(return_value="test-read-url"),
        **kwargs)

# The fixtures required to mock create()'s dependencies when a page does not exist in a db.
create_fixtures = pytest.mark.usefixtures('Language',
                                          'session_model')

@create_fixtures
def test_create_adds_page_to_db(Language):
    """
        This should add the new page to the database session, which is added only if it does not exit in a db.
        After successfully creating a new page it should redirect.
    """
    language = mock.Mock()
    Language.return_value = language

    request = _mock_request(matchdict={'language_name': 'test', 'public_group_id': 12345,
                                       'page_url': 'http://www.annotran_testing.com'})
    result = views.add_page(request)

    request.db.add.assert_called_once()
    assert isinstance(result, httpexceptions.HTTPRedirection)

# The fixtures required to mock create()'s dependencies for an existing page.
create_fixtures = pytest.mark.usefixtures('Page', 'Language',
                                          'session_model')

@create_fixtures
def test_create_redirects_to_page_read_page(Page, Language):
    """
        After successfully fetching mock Page and Language objects it
         should not add that page into db but it should redirect.
    """
    language = mock.Mock()
    Language.return_value = language
    page = mock.Mock(id=1)
    Page.return_value = page

    request = _mock_request(matchdict={'language_name': 'test', 'public_group_id': 12345,
                                       'page_url': 'http://www.annotran_testing.com'})
    result = views.add_page(request)
    assert not request.db.add.called
    assert isinstance(result, httpexceptions.HTTPRedirection)

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
def session_model(request):
    patcher = mock.patch('annotran.session.model')
    request.addfinalizer(patcher.stop)
    return patcher.start()

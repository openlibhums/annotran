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
        authenticated_userid = "acct:fred@hypothes.is"
    return mock.Mock(
        feature=feature or (lambda feature: True),
        registry=mock.Mock(settings=settings or {}),
        params=params, POST=params,
        authenticated_userid=authenticated_userid,
        route_url=route_url or mock.Mock(return_value="test-read-url"),
        **kwargs)


def _matchdict():
    return {"pubid": mock.sentinel.pubid, "slug": mock.sentinel.slug}


# The fixtures required to mock all of create()'s dependencies.
create_fixtures = pytest.mark.usefixtures('Page',
                                          'session_model')

@create_fixtures
def test_create_adds_page_to_db(Page):
    """This should add the new page to the database session."""
    page = mock.Mock(id=6)
    Page.return_value = page
    request = _mock_request(matchdict={'public_group_id': '12345', 'page': 'test_page'})

    views.add_page(request)

    #request.db.add.assert_called_once_with(page)

@create_fixtures
def test_create_redirects_to_page_read_page(Page):
    """After successfully creating a new page it should redirect."""
    page = mock.Mock(public_group_id='12345', page='page')
    Page.return_value = page
    request = _mock_request(matchdict={'public_group_id': '12345', 'page': 'test_page'})

    result = views.add_page(request)

    assert isinstance(result, httpexceptions.HTTPRedirection)

@create_fixtures
def test_create_with_non_ascii_name():
    views.add_page(_mock_request(matchdict={'public_group_id': 'abc', 'page': u"☆ ßüper Gröup ☆"}))

@pytest.fixture
def Page(request):
    patcher = mock.patch('annotran.pages.views.models.Page', autospec=True)
    request.addfinalizer(patcher.stop)
    return patcher.start()

@pytest.fixture
def session_model(request):
    patcher = mock.patch('annotran.session.model')
    request.addfinalizer(patcher.stop)
    return patcher.start()




# -*- coding: utf-8 -*-
import mock
import pytest
from pyramid import httpexceptions

from annotran.languages import views

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
    """Return a matchdict like the one the language_read route receives."""
    return {"pubid": mock.sentinel.pubid, "slug": mock.sentinel.slug}


# The fixtures required to mock all of create()'s dependencies.
create_fixtures = pytest.mark.usefixtures('LanguageSchema', 'Language',
                                          'session_model')

@create_fixtures
def test_create_adds_language_to_db(Language):
    """This should add the new language to the database session."""
    language = mock.Mock(id=6)
    Language.return_value = language
    request = _mock_request(matchdict={'public_group_id': '12345', 'language': 'test_language'})

    views.add_language(request)

    #request.db.add.assert_called_once_with(language)

@create_fixtures
def test_create_redirects_to_language_read_page(Language):
    """After successfully creating a new language it should redirect."""
    language = mock.Mock(public_group_id='12345', language='language')
    Language.return_value = language
    request = _mock_request(matchdict={'public_group_id': '12345', 'language': 'test_language'})

    result = views.add_language(request)

    assert isinstance(result, httpexceptions.HTTPRedirection)

@create_fixtures
def test_create_with_non_ascii_name():
    views.add_language(_mock_request(matchdict={'public_group_id': 'abc', 'language': u"☆ ßüper Gröup ☆"}))

@pytest.fixture
def LanguageSchema(request):
    patcher = mock.patch('annotran.languages.schemas.LanguageSchema', autospec=True)
    request.addfinalizer(patcher.stop)
    return patcher.start()

@pytest.fixture
def Language(request):
    patcher = mock.patch('annotran.languages.views.models.Language', autospec=True)
    request.addfinalizer(patcher.stop)
    return patcher.start()

@pytest.fixture
def session_model(request):
    patcher = mock.patch('annotran.session.model')
    request.addfinalizer(patcher.stop)
    return patcher.start()




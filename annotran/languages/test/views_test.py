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
        authenticated_userid = "acct:fred@annotran.com"
    return mock.Mock(
        feature=feature or (lambda feature: True),
        registry=mock.Mock(settings=settings or {}),
        params=params, POST=params,
        authenticated_userid=authenticated_userid,
        route_url=route_url or mock.Mock(return_value="test-read-url"),
        **kwargs)


def _matchdict():
    """Return a matchdict like the one the translation_read route receives."""
    return {"pubid": mock.sentinel.pubid, "slug": mock.sentinel.slug}


# The fixtures required to mock create()'s dependencies when a language does not exist in a db.
create_fixtures = pytest.mark.usefixtures('session_model')

@create_fixtures
def test_create_adds_language_to_db():
    """
        This should add the new language to the database session, whih is added only if it does not exit in a db.
        After successfully creating a new language it should redirect
    """
    request = _mock_request(matchdict={'public_group_id': '12345', 'language': 'zrrtgy'})
    result = views.add_language(request)
    request.db.add.assert_called_once()
    assert isinstance(result, httpexceptions.HTTPRedirection)


# The fixtures required to mock create()'s dependencies for an existing language.
create_fixtures = pytest.mark.usefixtures('LanguageSchema', 'Language',
                                          'session_model')
@create_fixtures
def test_create_redirects_to_translation_read_page(Language):
    """
        After successfully fetching a mock Language object it
         should not add that one into db but it should redirect.
    """
    language = mock.Mock(public_group_id='12345', language='language')
    Language.return_value = language
    request = _mock_request(matchdict={'public_group_id': '12345', 'language': 'test_language'})
    result = views.add_language(request)
    assert not request.db.add.called
    assert isinstance(result, httpexceptions.HTTPRedirection)

@create_fixtures
def test_create_with_non_ascii_name():
    request = _mock_request(matchdict={'public_group_id': 'abc', 'language': u"☆ ßüper Gröup ☆"})
    views.add_language(request)


@pytest.fixture
def LanguageSchema(request):
    patcher = mock.patch('annotran.languages.schemas.LanguageSchema', autospec=True)
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




# -*- coding: utf-8 -*-
import mock
import pytest
import types
import annotran

from pyramid import httpexceptions
from mock import PropertyMock
from mock import MagicMock
from annotran.translations import views


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


def test_add_translation_to_db():
    """
        This should add a new translation to the database session, which is added only if it does not exit in a db.
        After successfully creating a new translation it should redirect.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        propLang = PropertyMock(return_value=2897)
        type(language).id = propLang
        language.get_by_name = MagicMock(return_value=language)

        with mock.patch('annotran.pages.models.Page') as page:
            propPage = PropertyMock(return_value=2897)
            type(page).id = propPage
            page.get_by_uri = MagicMock(return_value=page)

            with mock.patch('h.groups.models.Group') as group:
                propGroup = PropertyMock(return_value=2897)
                type(group).id = propGroup
                group.get_by_pubid = MagicMock(return_value=group)

                request = _mock_request(matchdict={'public_group_id': '12345',
                                                   'language': 'test',
                                                   'page_url': 'http://www.annotran_test.com/'})
                result = views.add_translation(request)
                request.db.add.assert_called_once()
                assert isinstance(result, httpexceptions.HTTPRedirection)

def test_read_unauthenticated_user():
    """
        This should call "read_group" when trying to read
        translations for the selected combination of a group, page, and language.
        read_group method is mocked, so when it is called a group object is returned.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        propLang = PropertyMock(return_value=2897)
        type(language).id = propLang
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('h.groups.models.Group') as group:
            propGroup = PropertyMock(return_value=2897)
            type(group).id = propGroup
            group.get_by_pubid = MagicMock(return_value=group)

            request = mock.Mock(authenticated_userid = None,
                                matchdict={'public_group_id': '12345',
                                           'public_language_id': '12345'})
            result = views.read(request)
            assert result == None

def test_read_private_group_unauthenticated():
    """
        This should call "read_group" when trying to read
        translations for the selected combination of a group, page, and language.
        read_group method is mocked, so when it is called a group object is returned.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        propLang = PropertyMock(return_value=2897)
        type(language).id = propLang
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('h.groups.models.Group') as group:
            propGroup = PropertyMock(return_value=2897)
            type(group).id = propGroup
            group.get_by_pubid = MagicMock(return_value=group)

            request = _mock_request(authenticated_user=mock.Mock(groups=[]),
                                    matchdict={'public_group_id': '12345',
                                               'public_language_id': '12345'})
            result = views.read(request)
            assert result == None

def test_read_private_group_authenticated():
    """
        This should return None when trying to read
         translations for the selected combination of a group, page, and language, because group is
         not in the list of user's authorized groups.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        propLang = PropertyMock(return_value=2897)
        type(language).id = propLang
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('h.groups.models.Group') as group:
            propGroup = PropertyMock(return_value=2897)
            type(group).id = propGroup
            group.get_by_pubid = MagicMock(return_value=group)

            annotran.groups.views.read_group = MagicMock(return_value=group)

            request = _mock_request(authenticated_user=mock.Mock(groups=[group]),
                                    matchdict={'public_group_id': '12345',
                                               'public_language_id': '12345'})
            result = views.read(request)
            assert result == group

def test_read_public_group():
    """
        This should read translations for the selected combination of a group, page, and language (mainly call read_group).
        read_group method is mocked, so when it is called a group object is returned.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        propLang = PropertyMock(return_value=2897)
        type(language).id = propLang
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('h.groups.models.Group') as group:
            propGroup = PropertyMock(return_value=-1)
            type(group).id = propGroup
            group.get_by_pubid = MagicMock(return_value=group)
            annotran.groups.views.read_group = MagicMock(return_value=group)
            request = _mock_request(authenticated_user=mock.Mock(groups=[]),
                                    matchdict={'public_group_id': '12345',
                                               'public_language_id': '12345'})
            result = views.read(request)
            assert result == group

def test_add_translation_to_db_when_page_lang_group_none():
    """
        This should not add a new translation to the database session.
        If page, group or language is None, then it should return immediatelly.
    """
    request = _mock_request(matchdict={'public_group_id': '12345',
                                       'language': 'test',
                                       'page_url': 'http://www.annotran_test.com/'})
    result = views.add_translation(request)
    assert not request.db.add.called
    assert isinstance(result, types.DictType)


# The fixtures required to mock create()'s dependencies for an existing page.
create_fixtures = pytest.mark.usefixtures('Translation', 'Page', 'Language', 'Group',
                                          'session_model')

@create_fixtures
def test_create_redirects_to_translation_read_page(Page, Language, Group, Translation):
    """
        After successfully fetching mock objects Page, Language, and Translation it
         should not add that translation into db but it should redirect.
    """
    language = mock.Mock()
    Language.return_value = language

    page = mock.Mock()
    Page.return_value = page

    group = mock.Mock()
    Group.return_value = group

    translation = mock.Mock()
    Translation.return_value = translation

    request = _mock_request(matchdict={'public_group_id': '12345',
                                       'language': 'test',
                                       'page_url': 'http://www.annotran_test.com/'})
    result = views.add_translation(request)
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
def Translation(request):
    patcher = mock.patch('annotran.translations.models.Translation', autospec=True)
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

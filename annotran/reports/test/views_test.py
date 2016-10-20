# -*- coding: utf-8 -*-
import mock
import pytest

from pyramid import httpexceptions as exc
from mock import PropertyMock
from mock import MagicMock
from annotran.reports import views
from annotran.admin import *

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


def test_add_report_to_db():
    """
        This should add a new report to the database session.
        After successfully creating a new report it should redirect.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('annotran.pages.models.Page') as page:
            page.get_by_uri = MagicMock(return_value=page)

            with mock.patch('h.groups.models.Group') as group:
                group.get_by_pubid = MagicMock(return_value=group)

                with mock.patch('h.models.User') as user:
                    propUser = PropertyMock(return_value=2897)
                    type(user).id = propUser
                    user.get_by_username = MagicMock(return_value=user)

                    with mock.patch('annotran.translations.models.Translation') as translation:
                        propPage = PropertyMock(return_value=2897)
                        type(translation).page_id = propPage

                        propLang = PropertyMock(return_value=2897)
                        type(translation).language_id = propLang

                        propGroup = PropertyMock(return_value=2897)
                        type(translation).group_id = propGroup

                        translation.get_translation = MagicMock(return_value=translation)

                        request = _mock_request(authenticated_user=mock.Mock(username="test"),
                                                matchdict={'public_language_id': '12345',
                                                           'public_group_id': '12345',
                                                           'user_id': '12345',
                                                           'page_uri': 'http://www.annotran_test.com/'})
                        result = views.add_report(request)
                        request.db.add.assert_called_once()
                        assert result == {}

def test_add_report_to_db_pg_auth_rep_group_lang_none():
    """
        This should raise HTTPNotFound as all page, author, reporter, group, and language is None.
    """
    request = _mock_request(authenticated_user=mock.Mock(username="test"),
                            matchdict={'public_language_id': '12345',
                                       'public_group_id': '12345',
                                       'user_id': '12345',
                                       'page_uri': 'http://www.annotran_test.com/'})
    with pytest.raises(exc.HTTPNotFound):
        views.add_report(request)

def test_add_report_to_db_translation_none():
    """
        This should raise HTTPNotFound as translation is None.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('annotran.pages.models.Page') as page:
            page.get_by_uri = MagicMock(return_value=page)

            with mock.patch('h.groups.models.Group') as group:
                group.get_by_pubid = MagicMock(return_value=group)

                with mock.patch('h.models.User') as user:
                    user.get_by_username = MagicMock(return_value=user)

                    with mock.patch('annotran.translations.models.Translation') as translation:
                        translation.get_translation = MagicMock(return_value=None)

                        request = _mock_request(authenticated_user=mock.Mock(username="test"),
                                                matchdict={'public_language_id': '12345',
                                                           'public_group_id': '12345',
                                                           'user_id': '12345',
                                                           'page_uri': 'http://www.annotran_test.com/'})
                        with pytest.raises(exc.HTTPNotFound):
                            views.add_report(request)

def test_add_existing_report_to_db():
    """
        This should not add a new report to the database session as the one already exists.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('annotran.pages.models.Page') as page:
            page.get_by_uri = MagicMock(return_value=page)

            with mock.patch('h.groups.models.Group') as group:
                group.get_by_pubid = MagicMock(return_value=group)

                with mock.patch('h.models.User') as user:
                    user.get_by_username = MagicMock(return_value=user)

                    with mock.patch('annotran.translations.models.Translation') as translation:
                        translation.get_translation = MagicMock(return_value=translation)

                        with mock.patch('annotran.reports.models.Report') as report:
                            report.get_report = MagicMock(return_value=report)

                            request = _mock_request(authenticated_user=mock.Mock(username="test"),
                                                    matchdict={'public_language_id': '12345',
                                                               'public_group_id': '12345',
                                                               'user_id': '12345',
                                                               'page_uri': 'http://www.annotran_test.com/'})
                            result = views.add_report(request)
                            assert not request.db.add.called
                            assert isinstance(result, exc.HTTPBadRequest)

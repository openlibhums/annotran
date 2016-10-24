# -*- coding: utf-8 -*-
import mock

from mock import PropertyMock
from mock import MagicMock
from annotran import admin
from annotran.admin import *
from pyramid import httpexceptions as exc

_SENTINEL = object()

def _mock_request(feature=None, settings=None, params=None,
                  authenticated_userid=_SENTINEL, route_url=None, **kwargs):
    """Return a mock Pyramid request object."""
    params = params or {"foo": "bar"}
    if authenticated_userid is _SENTINEL:
        authenticated_userid = "acct:gam@annotran.com"
    return mock.Mock(
        feature=feature or (lambda feature: True),
        registry=mock.Mock(settings=settings or {}),
        params=params, POST=params,
        authenticated_userid=authenticated_userid,
        route_url=route_url or mock.Mock(return_value="test-read-url"),
        **kwargs)


def test_reports_view():
    """
        This should return a context dictionary (of length 8) for the translation template.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('h.groups.models.Group') as group:
            group.get_by_pubid = MagicMock(return_value=group)
            annotran.groups.views.read_group = MagicMock(return_value=group)

            request = _mock_request(authenticated_user=mock.Mock(username="test"),
                                    matchdict={'page': 'http://www.annotran_test.com/',
                                               'language': '12345',
                                               'group': '12345',
                                               'user': 'acct:gam@127.0.0.1',
                                               'report': 'report'})
            result = reports_view(request)
            assert isinstance(result, dict)
            assert result.__len__() == 8

def test_reports_delete():
    """
        This should invoke deletion of a report, translation (all annotations), and all votes.
        After that it should redirect.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('h.groups.models.Group') as group:
            group.get_by_pubid = MagicMock(return_value=group)

            with mock.patch('annotran.pages.models.Page') as page:
                page.get_by_uri = MagicMock(return_value=page)

                with mock.patch('annotran.translations.models.Translation') as translation:
                    translation.get_translation = MagicMock(return_value=translation)

                    h.accounts.models.User.query.filter = MagicMock(return_value=None)

                    admin.delete_annotations = MagicMock(return_value=None)

                    admin.delete_report = MagicMock(return_value=None) # this methos should be outside of admin.py (in reports/views)?

                    annotran.votes.models.Vote.delete_votes = MagicMock(return_value=None)

                    request = _mock_request(authenticated_user=mock.Mock(username="test"),
                                            matchdict={'page': 'http://www.annotran_test.com/',
                                                       'language': '12345',
                                                       'group': '12345',
                                                       'user': 'acct:gam@127.0.0.1'})

                    result = reports_delete(request)
                    admin.delete_annotations.assert_called_once()
                    admin.delete_report.assert_called_once()
                    annotran.votes.models.Vote.delete_votes.assert_called_once()
                    assert isinstance(result, exc.HTTPRedirection)

def test_reports_delete_with_blocking():
    """
        This should invoke deletion of a report, translation (all annotations), and all votes,
        and additionally change the user activation_id.
        After that it should redirect.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('h.groups.models.Group') as group:
            group.get_by_pubid = MagicMock(return_value=group)

            with mock.patch('annotran.pages.models.Page') as page:
                page.get_by_uri = MagicMock(return_value=page)

                with mock.patch('annotran.translations.models.Translation') as translation:
                    translation.get_translation = MagicMock(return_value=translation)

                    with mock.patch('h.accounts.models.User') as user:
                        propUser = PropertyMock(return_value=2897)
                        type(user).activation_id = propUser
                        user.get_by_username = MagicMock(return_value=user)
                        user.query.filter = MagicMock(return_value=user)

                        admin.delete_annotations = MagicMock(return_value=None)

                        admin.delete_report = MagicMock(return_value=None) # this methos should be outside of admin.py (in reports/views)?

                        annotran.votes.models.Vote.delete_votes = MagicMock(return_value=None)

                        request = _mock_request(authenticated_user=mock.Mock(username="test"),
                                                matchdict={'page': 'http://www.annotran_test.com/',
                                                           'language': '12345',
                                                           'group': '12345',
                                                           'user': 'acct:gam@127.0.0.1'})
                        result = reports_delete(request, True)
                        admin.delete_annotations.assert_called_once()
                        admin.delete_report.assert_called_once()
                        annotran.votes.models.Vote.delete_votes.assert_called_once()
                        request.db.flush.assert_called_once()
                        assert isinstance(result, exc.HTTPRedirection)

def test_reports_delete_block():
    """
        This should invoke admin.reports_delete(request, block=True)
    """
    request = _mock_request(authenticated_user=mock.Mock())
    admin.reports_delete = MagicMock(return_value=None)
    reports_delete_block(request)
    admin.reports_delete.assert_called_once()

def test_reports_delete_report():
    """
        This should invoke deletion of a report only, and without blocking a user.
        After that it should redirect.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('h.groups.models.Group') as group:
            group.get_by_pubid = MagicMock(return_value=group)

            with mock.patch('annotran.pages.models.Page') as page:
                page.get_by_uri = MagicMock(return_value=page)

                with mock.patch('annotran.translations.models.Translation') as translation:
                    translation.get_translation = MagicMock(return_value=translation)

                    with mock.patch('annotran.reports.models.Report') as report:
                        report.get_by_id = MagicMock(return_value=report)

                        with mock.patch('h.accounts.models.User') as user:
                            user.query.filter = MagicMock(return_value=user)

                            admin.delete_report = MagicMock(return_value=None) # this methos should be outside of admin.py (in reports/views)?

                            request = _mock_request(authenticated_user=mock.Mock(username="test"),
                                            matchdict={'page': 'http://www.annotran_test.com/',
                                                       'language': '12345',
                                                       'report': '12345',
                                                       'group': '12345'})

                            result = reports_delete_report(request)
                            admin.delete_report.assert_called_once()
                            assert not request.db.flush.called
                            assert isinstance(result, exc.HTTPRedirection)

def test_reports_delete_report_with_blocking():
    """
        This should invoke deletion of a report only, and block a user by changing user's activation_id.
        After that it should redirect.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('h.groups.models.Group') as group:
            group.get_by_pubid = MagicMock(return_value=group)

            with mock.patch('annotran.pages.models.Page') as page:
                page.get_by_uri = MagicMock(return_value=page)

                with mock.patch('annotran.translations.models.Translation') as translation:
                    translation.get_translation = MagicMock(return_value=translation)

                    with mock.patch('annotran.reports.models.Report') as report:
                        report.get_by_id = MagicMock(return_value=report)

                        with mock.patch('h.accounts.models.User') as user:
                            propUser = PropertyMock(return_value=2897)
                            type(user).activation_id = propUser
                            user.get_by_username = MagicMock(return_value=user)
                            user.query.filter = MagicMock(return_value=user)

                            admin.delete_report = MagicMock(return_value=None) # this methos should be outside of admin.py (in reports/views)?

                            request = _mock_request(authenticated_user=mock.Mock(username="test"),
                                            matchdict={'page': 'http://www.annotran_test.com/',
                                                       'language': '12345',
                                                       'report': '12345',
                                                       'group': '12345'})

                            result = reports_delete_report(request, True)
                            admin.delete_report.assert_called_once()
                            request.db.flush.assert_called_once()
                            assert isinstance(result, exc.HTTPRedirection)

def test_reports_delete_block_report():
    """
        This should invoke admin.reports_delete_report(request, block=True)
    """
    request = _mock_request(authenticated_user=mock.Mock())
    admin.reports_delete_report = MagicMock(return_value=None)
    reports_delete_block_report(request)
    admin.reports_delete_report.assert_called_once()

def test_reports_index():
    """
        This should query all reports from a database and return a context dictionary (of length 1 - as there is only one report added) for it.
    """
    reports = []
    with mock.patch('annotran.languages.models.Language') as language:
        language.get_by_id = MagicMock(return_value=language)

        with mock.patch('h.groups.models.Group') as group:
            group.get_by_id = MagicMock(return_value=group)

            with mock.patch('annotran.pages.models.Page') as page:
                page.get_by_id = MagicMock(return_value=page)

                with mock.patch('annotran.translations.models.Translation') as translation:
                    translation.get_by_composite_id = MagicMock(return_value=translation)

                    with mock.patch('annotran.reports.models.Report') as report:
                        propReport = PropertyMock(return_value=2897)
                        type(report).id = propReport
                        reports.append(report)
                        report.get_all = MagicMock(return_value=reports)

                        with mock.patch('h.accounts.models.User') as user:
                            propUser = PropertyMock(return_value=2897)
                            type(user).id = propUser
                            user.get_by_username = MagicMock(return_value=user)
                            user.query.filter = MagicMock(return_value=user)

                            h.util.userid_from_username = MagicMock(return_value="12345")

                            request = _mock_request(authenticated_user=mock.Mock())
                            result = reports_index(request)
                            assert isinstance(result, dict)
                            assert result.__len__() == 1
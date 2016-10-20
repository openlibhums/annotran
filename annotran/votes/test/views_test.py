# -*- coding: utf-8 -*-
import mock
import pytest

from pyramid import httpexceptions
from mock import PropertyMock
from mock import MagicMock
from annotran.votes import views
from pyramid import httpexceptions as exc


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

def test_add_vote_to_db_unauthenticated_user():
    """
        This should raise HTTPNotFound because of unauthenticated user.
    """
    request = _mock_request(authenticated_user=None)
    with pytest.raises(httpexceptions.HTTPNotFound):
        views.add_vote(request)

def test_add_vote_to_db_authenticated_user():
    """
        This should add a new vote to the database session. Since a new vote is being added,
        a deletion of the previous vote value will not be initiated.
        After successfully adding a new vote it should redirect.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        propLang = PropertyMock(return_value=2897)
        type(language).id = propLang
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('annotran.pages.models.Page') as page:
            propPage = PropertyMock(return_value=2897)
            type(page).id = propPage
            page.get_by_uri = MagicMock(return_value=page)

            with mock.patch('h.groups.models.Group') as group:
                propGroup = PropertyMock(return_value=2897)
                type(group).id = propGroup
                group.get_by_pubid = MagicMock(return_value=group)

                with mock.patch('h.models.User') as user:
                    propUser = PropertyMock(return_value=2897)
                    type(user).id = propUser
                    user.get_by_username = MagicMock(return_value=user)

                    request = _mock_request(matchdict={'page_uri': 'http://www.annotran_test.com',
                                                       'public_group_id': "12345",
                                                       'public_language_id': "12345",
                                                       'score': 5,
                                                       'username':"test_username"},
                                            authenticated_user=mock.Mock(id=2, username="test2", uid="test2"))
                    result = views.add_vote(request)
                    request.db.add.assert_called_once()
                    assert not request.db.delete.called
                    assert isinstance(result, httpexceptions.HTTPRedirection)

def test_add_over_existing_vote_to_db():
    """
        This should delete an existing vote from the db and add a new one.
        After successfully adding a new vote it should redirect.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('annotran.pages.models.Page') as page:
            page.get_by_uri = MagicMock(return_value=page)

            with mock.patch('h.groups.models.Group') as group:
                group.get_by_pubid = MagicMock(return_value=group)

                with mock.patch('h.models.User') as user:
                    user.get_by_username = MagicMock(return_value=user)

                    with mock.patch('annotran.votes.models.Vote') as vote:
                        vote.get_vote = MagicMock(return_value=vote)

                        request = _mock_request(matchdict={'page_uri': 'http://www.annotran_test.com',
                                                           'public_group_id': "12345",
                                                           'public_language_id': "12345",
                                                           'score': 5,
                                                           'username':"test_username"},
                                                authenticated_user=mock.Mock(id=2, username="test2", uid="test2"))
                        result = views.add_vote(request)
                        request.db.delete.assert_called_once()
                        request.db.add.assert_called_once()
                        assert isinstance(result, httpexceptions.HTTPRedirection)

def test_add_vote_to_db_authenticated_user_objects_none():
    """
        This should raise HTTPNotFound as all page, author, voter, group, and language are None.
    """
    request = _mock_request(matchdict={'page_uri': 'http://www.annotran_test.com',
                                       'public_group_id': "12345",
                                       'public_language_id': "12345",
                                       'score': 5,
                                       'username':"test_username"},
                            authenticated_user=mock.Mock(id=2, username="test2", uid="test2"))
    with pytest.raises(httpexceptions.HTTPNotFound):
        views.add_vote(request)

def test_delete_vote_unauthenticated_user():
    """
        This should raise HTTPNotFound because of unauthenticated user.
    """
    request = _mock_request(authenticated_user=None)
    with pytest.raises(httpexceptions.HTTPNotFound):
        views.delete_vote(request)

def test_delete_vote_authenticated_user():
    """
        This should delete an existing vote from the db.
    """
    with mock.patch('annotran.languages.models.Language') as language:
        language.get_by_public_language_id = MagicMock(return_value=language)

        with mock.patch('annotran.pages.models.Page') as page:
            page.get_by_uri = MagicMock(return_value=page)

            with mock.patch('h.groups.models.Group') as group:
                group.get_by_pubid = MagicMock(return_value=group)

                with mock.patch('h.models.User') as user:
                    user.get_by_username = MagicMock(return_value=user)

                    with mock.patch('annotran.votes.models.Vote') as vote:
                        vote.delete_votes = MagicMock(return_value=vote)

                        request = _mock_request(matchdict={'page_uri': 'http://www.annotran_test.com',
                                                           'public_group_id': "12345",
                                                           'public_language_id': "12345"},
                                                authenticated_user=mock.Mock(id=2, username="test2", uid="test2"))
                        result = views.delete_vote(request)
                        assert result == {}

def test_delete_vote_authenticated_user_objects_none():
    """
        This should raise HTTPNotFound as all user, page, group, and language are None.
    """
    request = _mock_request(matchdict={'page_uri': 'http://www.annotran_test.com',
                                       'public_group_id': "12345",
                                       'public_language_id': "12345"},
                            authenticated_user=mock.Mock(id=2, username="test2", uid="test2"))
    with pytest.raises(httpexceptions.HTTPNotFound):
        views.delete_vote(request)
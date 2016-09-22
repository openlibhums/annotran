import urllib

import annotran
import annotran.languages.models
import annotran.pages.models
import h
import h.groups.models
import h.models
import models
from h import i18n
from pyramid import httpexceptions as exc
from pyramid.view import view_config

_ = i18n.TranslationString


@view_config(route_name='vote_add', request_method='POST')
def add_vote(request):
    """
    Add a vote to the database
    :param request: the current request object
    :return: a redirect to language read
    """
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    voter = request.authenticated_user
    if voter is None:
        raise exc.HTTPNotFound()

    page_url = urllib.unquote(urllib.unquote(request.matchdict["page_id"]))
    public_group_id = request.matchdict['public_group_id']
    public_language_id = request.matchdict["public_language_id"]
    score = request.matchdict["score"]
    user_id = request.matchdict['user_id']

    author = h.models.User.get_by_username(user_id)
    group = h.groups.models.Group.get_by_pubid(public_group_id)
    page = annotran.pages.models.Page.get_by_uri(page_url)
    voter = h.models.User.get_by_username(request.authenticated_user.username)

    language = annotran.languages.models.Language.get_by_public_language_id(public_language_id, page)

    if language is None or page is None:
        raise exc.HTTPNotFound()

    vote = models.Vote.get_vote(page, language, group, author, voter)

    # storing last selected value only
    if vote:
        request.db.delete(vote)
        request.db.flush()
    vote = models.Vote(score, page, language, group, author, voter)
    request.db.add(vote)
    request.db.flush()

    url = request.route_url('language_read', public_language_id=language.pubid, public_group_id=public_group_id)
    return exc.HTTPSeeOther(url)


@view_config(route_name='vote_delete', request_method='POST')
def delete_vote(request):
    """
    Delete a vote from the database
    :param request: the current request object
    :return: a redirect to language read
    """
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    public_language_id = request.matchdict["public_language_id"]
    public_group_id = request.matchdict['public_group_id']
    page_url = urllib.unquote(urllib.unquote(request.matchdict['page_id']))

    page = annotran.pages.models.Page.get_by_uri(page_url)
    language = annotran.languages.models.Language.get_by_public_language_id(public_language_id, page)

    # only authenticated used can delete translations and consequently their scores
    user = h.models.User.get_by_username(request.authenticated_user.username)
    group = h.groups.models.Group.get_by_pubid(public_group_id)

    models.Vote.delete_votes(page, language, group, user)
    request.db.flush()

    url = request.route_url('language_read', pubid=language.pubid, groupubid=public_group_id)
    return exc.HTTPSeeOther(url)


def includeme(config):
    """
    Pyramid's router configuration
    :param config: the configuration object to which to add our routes
    :return: None
    """
    config.add_route('vote_add', 'votes/{user_id}/{public_group_id}/{public_language_id}/{page_id}/{score}/addVote')
    config.add_route('vote_delete', 'votes/{public_group_id}/{public_language_id}/{page_id}/deleteVote')
    config.scan(__name__)

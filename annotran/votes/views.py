import urllib

from pyramid import httpexceptions as exc
from pyramid.view import view_config
from h import i18n
from annotran.util import util

import models
import annotran
import urllib
import h


_ = i18n.TranslationString


@view_config(route_name='vote_add',
             request_method='POST')
def addVote(request):
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    voter = request.authenticated_user
    if voter is None:
        raise exc.HTTPNotFound()

    languageId = request.matchdict["languageId"]
    pageId = request.matchdict["pageId"]
    score = request.matchdict["score"]
    userId = request.matchdict['userId']
    groupPubid = request.matchdict['groupId']

    pageId = urllib.unquote(urllib.unquote(pageId))
    page = annotran.pages.models.Page.get_by_uri(pageId)
    language = annotran.languages.models.Language.get_by_public_language_id(languageId, page)
    author = h.models.User.get_by_username(userId)
    voter = h.models.User.get_by_username(request.authenticated_user.username)
    group = h.groups.models.Group.get_by_pubid(groupPubid)


    if language is None or page is None:
        raise exc.HTTPNotFound()

    vote = models.Vote.get_vote(page, language, group, author, voter)

    #storing last selected value only
    if vote:
        request.db.delete(vote)
        request.db.flush()
    vote = models.Vote(score, page, language, group, author, voter)
    request.db.add(vote)
    request.db.flush()

    #url = request.route_url('vote_read', userid=userId, languageid=languageId, pageid=request.matchdict["pageId"])
    url = request.route_url('language_read', pubid=language.pubid, groupubid=groupPubid)
    return exc.HTTPSeeOther(url)

@view_config(route_name='vote_delete',
             request_method='POST')
def deleteVote(request):
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    languageId = request.matchdict["languageId"]
    groupPubid = request.matchdict['groupId']
    pageId = urllib.unquote(urllib.unquote(request.matchdict['pageId']))

    page = annotran.pages.models.Page.get_by_uri(pageId)
    language = annotran.languages.models.Language.get_by_public_language_id(languageId, page)
    user = h.models.User.get_by_username(request.authenticated_user.username) #only authenticated used can delete translations and consequently their scores
    group = h.groups.models.Group.get_by_pubid(groupPubid)

    models.Vote.delete_votes( page, language, group, user)
    request.db.flush()

    url = request.route_url('language_read', pubid=language.pubid, groupubid=groupPubid)
    return exc.HTTPSeeOther(url)

@view_config(route_name='vote_read', request_method='GET')
def read(request):
    url=util.get_url_from_request(request)
    languageId = request.matchdict["languageId"]
    page = annotran.pages.models.Page.get_by_uri(url)
    language = annotran.languages.models.Language.get_by_public_language_id(languageId, page)
    if not request.authenticated_userid:
        return None

    models.Vote.get_votes_for_authors(page, language)

    return None

def includeme(config):
    config.add_route('vote_add', 'votes/{userId}/{groupId}/{languageId}/{pageId}/{score}/addVote')
    config.add_route('vote_delete', 'votes/{groupId}/{languageId}/{pageId}/deleteVote')
    config.add_route('vote_read', '/votes/{userid}/{languageid}/{pageid}')
    config.scan(__name__)
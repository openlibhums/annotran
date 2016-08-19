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

    pageId = urllib.unquote(urllib.unquote(pageId))
    page = annotran.pages.models.Page.get_by_uri(pageId)
    language = annotran.languages.models.Language.get_by_pubid(languageId, page)
    user = h.models.User.get_by_username(userId)

    vote = models.Vote.get_by_voter(page, language, user, voter)

    if not vote:
        if language and page:
            vote = models.Vote(score=score, page=page, language=language, user=user, voter=voter)
        else:
            vote = models.Vote(vote=score)
        request.db.add(vote)
        request.db.flush()
    else:
        if voter and language and page:
            vote.relUser.append(voter)
            vote.relLanguage.append(language)
            vote.relPage.append(page)

    url = request.route_url('vote_read', userid=userId, languageid=languageId, pageid=request.matchdict["pageId"])
    return exc.HTTPSeeOther(url)

@view_config(route_name='vote_read', request_method='GET')
def read(request):
    url=util.get_url_from_request(request)
    page = annotran.pages.models.Page.get_by_uri(url)
    if not request.authenticated_userid:
        return None
    return None

def includeme(config):
    config.add_route('vote_add', 'votes/{userId}/{languageId}/{pageId}/{score}/addVote')
    config.add_route('vote_read', '/votes/{userid}/{languageid}/{pageid}')
    config.scan(__name__)

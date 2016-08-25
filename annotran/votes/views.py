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

    languageId = request.matchdict["languageId"]
    pageId = request.matchdict["pageId"]
    score = request.matchdict["score"]
    userId = request.matchdict['userId']

    pageId = urllib.unquote(urllib.unquote(pageId))
    page = annotran.pages.models.Page.get_by_uri(pageId)
    language = annotran.languages.models.Language.get_by_pubid(languageId, page)
    author = h.models.User.get_by_username(userId)
    voter = h.models.User.get_by_username(request.authenticated_user.username)

    vote = models.Vote.get_by_vote(score)

    if language is None or page is None:
         raise exc.HTTPNotFound()

    voted=None
    if vote is None:
        vote = models.Vote(score=score, page=page, language=language, author=author, voter=voter)
        request.db.add(vote)
        request.db.flush()
    else:
        voted = models.Vote.get_by_author_voter(page, language, author, voter)
        if voted is None:
            vote.relUser.append(author)
            vote.relUser.append(voter)
            vote.relLanguage.append(language)
            vote.relPage.append(page)
            request.db.flush()
    if voted is None:
        author_type = models.UserType.get_by_type("author")
        voter_type = models.UserType.get_by_type("voter")
        if author_type is None: #it's sufficient to check for one type only
            author_type = models.UserType(type="author", user=author)
            voter_type = models.UserType(type="voter", user=voter)
            request.db.add(author_type)
            request.db.add(voter_type)
        else:
            author_type.relUserType.append(author)
            voter_type.relUserType.append(voter)
        request.db.flush()

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

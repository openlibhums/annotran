import urllib

from pyramid import httpexceptions as exc
from pyramid.view import view_config
from h import i18n
from annotran.util import util

import annotran
import urllib
import h

import annotran.pages.models
import annotran.languages.models
import h.models
import h.groups.models
import annotran.reports.models


@view_config(route_name='report_add', request_method='POST')
def addReport(request):
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    reporter = request.authenticated_user
    if reporter is None:
        raise exc.HTTPNotFound()

    languageId = request.matchdict["languageId"]
    pageId = request.matchdict["pageId"]
    userId = request.matchdict['userId']
    groupPubid = request.matchdict['groupId']

    pageId = urllib.unquote(urllib.unquote(pageId))
    page = annotran.pages.models.Page.get_by_uri(pageId)
    language = annotran.languages.models.Language.get_by_pubid(languageId, page)
    author = h.models.User.get_by_username(userId)
    reporter = h.models.User.get_by_username(request.authenticated_user.username)
    group = h.groups.models.Group.get_by_pubid(groupPubid)


    if language is None or page is None:
        raise exc.HTTPNotFound()

    report = annotran.reports.models.Report.get_report(page, language, group, author, reporter)

    #storing last selected value only
    if report:
        request.db.delete(report)
        request.db.flush()

    report = annotran.reports.models.Report(page, language, group, author, reporter)
    request.db.add(report)
    request.db.flush()

    return exc.HTTPSeeOther("/admin/reports")


def includeme(config):
    config.add_route('report_add', 'reports/{userId}/{groupId}/{languageId}/{pageId}/addReport')
    config.scan(__name__)
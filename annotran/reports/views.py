import urllib

import annotran
import annotran.languages.models
import annotran.mailer
import annotran.pages.models
import annotran.reports.models
import annotran.views
import h
import h.groups.models
import h.models
from pyramid import httpexceptions as exc
from pyramid.view import view_config


@view_config(route_name='report_add', request_method='POST', renderer='annotran:templates/home.html.jinja2')
def add_report(request):
    """
    Add an abuse report to the database
    :param request: a request object
    :return: a redirect to the abuse reports page
    """
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    reporter = request.authenticated_user
    if reporter is None:
        raise exc.HTTPNotFound()

    public_language_id = request.matchdict["public_language_id"]
    page_url = urllib.unquote(urllib.unquote(request.matchdict["page_uri"]))
    public_group_id = request.matchdict['public_group_id']
    user_id = request.matchdict['user_id']

    page = annotran.pages.models.Page.get_by_uri(page_url)
    language = annotran.languages.models.Language.get_by_public_language_id(public_language_id, page)
    author = h.models.User.get_by_username(user_id)
    reporter = h.models.User.get_by_username(request.authenticated_user.username)
    group = h.groups.models.Group.get_by_pubid(public_group_id)

    if language is None or page is None:
        raise exc.HTTPNotFound()

    report = annotran.reports.models.Report.get_report(page, language, group, author, reporter)

    # storing last selected value only
    if report:
        request.db.delete(report)
        request.db.flush()

    report = annotran.reports.models.Report(page, language, group, author, reporter)
    request.db.add(report)
    request.db.flush()

    reports = request.route_url('admin_reports')

    body_text = u'Hello,\n\nA new abuse report has been filed. ' \
                u'Please see <a href="{0}">{0}</a>.\n\nAnnotran'.format(reports)

    annotran.mailer.send(request, subject=u'A new abuse report has been filed',
                         recipients=[annotran.views.Shared.support_address],
                         body=body_text)

    return {}


def includeme(config):
    """
    Pyramid's router configuration
    :param config: the configuration object to which to push our routes
    :return: None
    """
    config.add_route('report_add', 'reports/{user_id}/{public_group_id}/{public_language_id}/{page_uri}/addReport')
    config.scan(__name__)

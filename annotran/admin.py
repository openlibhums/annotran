import urllib

import annotran
import annotran.groups.views
import annotran.translations.models
import annotran.languages.models
import annotran.pages.models
import annotran.reports.models
import annotran.votes.models
import h
import h.accounts.models
import h.groups.models
import h.groups.views
import h.util
from annotran.api.search import core as annotran_search
from pyramid import httpexceptions as exc
from pyramid import view


def delete_annotations(request, group, language=None, search_url=None, user=None):
    """
    Delete a set of annotations from Elastic search
    :param request: a request object
    :param group: a group object
    :param language: a language object
    :param search_url: the URL on which to operate
    :param user: a username string
    :return: None
    """

    if group is None:
        public_group_id = "__world__"
    else:
        public_group_id = group.pubid

    parameters = {"group": public_group_id, "limit": 1000}

    if language:
        parameters['language'] = language.pubid

    if search_url:
        parameters['uri'] = search_url

    if user:
        parameters['user'] = user

    annotran_search.delete(request,
                           private=True,
                           params=parameters)


@view.view_config(route_name='admin_reports',
                  request_method='GET',
                  renderer='annotran:templates/admin/reports.html.jinja2',
                  permission='admin_reports')
def reports_index(_):
    """
    View a list of reports.
    :param _: a request object
    :return: a context list for the
    """
    reports = annotran.reports.models.Report.get_all()

    ret_list = []

    for report in reports:
        translation = annotran.translations.models.Translation.get_by_id(report.translation_id)

        ret_dict = {'url': annotran.pages.models.Page.get_by_id(translation.page_id).uri,
                    'group': h.groups.models.Group.get_by_id(translation.group_id).pubid,
                    'language': annotran.languages.models.Language.get_by_id(translation.language_id).pubid,
                    'author': h.util.userid_from_username(h.accounts.models.User.query.filter(
                        h.accounts.models.User.id == report.author_id).first().username, request=_),
                    'reporter': h.util.userid_from_username(h.accounts.models.User.query.filter(
                        h.accounts.models.User.id == report.reporter_id).first().username, request=_),
                    'id': report.id}

        ret_dict['url_encoded'] = urllib.quote(urllib.quote(ret_dict["url"], safe=''), safe='')

        ret_list.append(ret_dict)

    return {'reports': ret_list}


@view.view_config(route_name='admin_delete_block_report',
                  request_method='GET',
                  renderer='annotran:templates/admin/translation.html.jinja2',
                  permission='admin_delete_block_report')
def reports_delete_block_report(request):
    """
    A view that deletes a report and blocks the user who reported it
    :param request: a request object
    :return: a redirect to the reports home page
    """
    return reports_delete_report(request, block=True)


@view.view_config(route_name='admin_delete_report',
                  request_method='GET',
                  renderer='annotran:templates/admin/translation.html.jinja2',
                  permission='admin_delete_report')
def reports_delete_report(request, block=False):
    """
    A view to delete a report but leave the translation in tact
    :param request: a request object
    :param block: whether or not to block the user who made the report
    :return: a redirect to the reports home page
    """
    url = urllib.unquote(urllib.unquote(request.matchdict["page"]))
    page = annotran.pages.models.Page.get_by_uri(url)
    public_language_id = request.matchdict["language"]
    language = annotran.languages.models.Language.get_by_public_language_id(public_language_id)

    report = annotran.reports.models.Report.get_by_id(request.matchdict["report"])

    user_object = h.accounts.models.User.query.filter(
        h.accounts.models.User.username == report.Reporter.username).first()

    public_group_id = request.matchdict["group"]
    group = h.groups.models.Group.get_by_pubid(public_group_id)

    translation = annotran.translations.models.Translation.get_translation(page, language, group)

    if block:
        dummy_user = h.accounts.models.User.get_by_username("ADummyUserForGroupCreation")
        user_object.activation_id = dummy_user.activation_id

        request.db.flush()

    delete_report(translation, user_object, reporter=True)

    return exc.HTTPSeeOther("/admin/reports")


@view.view_config(route_name='admin_delete_block_translation',
                  request_method='GET',
                  renderer='annotran:templates/admin/translation.html.jinja2',
                  permission='admin_delete_block_translation')
def reports_delete_block(request):
    """
    Delete a report and a translation and block the user who made the translation
    :param request: a request object
    :return: a redirect to the reports home page
    """
    return reports_delete(request, block=True)


@view.view_config(route_name='admin_delete_translation',
                  request_method='GET',
                  renderer='annotran:templates/admin/translation.html.jinja2',
                  permission='admin_delete_translation')
def reports_delete(request, block=False):
    """
    Delete a report and a a translation
    :param request: a request object
    :param block: whether or not to block the user who owns the translation
    :return: a redirect to the reports home page
    """
    url = urllib.unquote(urllib.unquote(request.matchdict["page"]))
    user = request.matchdict["user"]
    public_language_id = request.matchdict["language"]
    public_group_id = request.matchdict["group"]

    page = annotran.pages.models.Page.get_by_uri(url)
    language = annotran.languages.models.Language.get_by_public_language_id(public_language_id)
    group = h.groups.models.Group.get_by_pubid(public_group_id)

    translation = annotran.translations.models.Translation.get_translation(page, language, group)

    user_object = h.accounts.models.User.query.filter(
        h.accounts.models.User.username == h.util.split_user(user)["username"]).first()

    delete_annotations(request, group=group, language=language, search_url=url, user=user)

    delete_report(translation, user_object)

    annotran.votes.models.Vote.delete_votes(page, language, group, user_object)

    if block:
        dummy_user = h.accounts.models.User.get_by_username("ADummyUserForGroupCreation")
        user_object.activation_id = dummy_user.activation_id

        request.db.flush()

    return exc.HTTPSeeOther("/admin/reports")


def delete_report(translation, user, reporter=False):
    """
    Delete all reports pertaining to a translation.
    :param translation: the translation object
    :param user: the user object of the translation
    :param reporter: if true, deletes a report where the reporter is equal to user
    :return: None
    """
    # NB this function deletes all reports pertaining to this translation
    if not reporter:
        annotran.reports.models.Report.query.filter(annotran.reports.models.Report.translation_id == translation.id,
                                                    annotran.reports.models.Report.author == user).delete()
    else:
        annotran.reports.models.Report.query.filter(annotran.reports.models.Report.translation_id == translation.id,
                                                    annotran.reports.models.Report.Reporter == user).delete()


@view.view_config(route_name='admin_view_translation',
                  request_method='GET',
                  renderer='annotran:templates/admin/translation.html.jinja2',
                  permission='admin_view_translation')
def reports_view(request):
    """
    A view to inspect a translation
    :param request: a request object
    :return: a context dictionary for the translation template
    """
    url = urllib.unquote(urllib.unquote(request.matchdict["page"]))

    public_language_id = request.matchdict["language"]
    language = annotran.languages.models.Language.get_by_public_language_id(public_language_id)

    public_group_id = request.matchdict["group"]
    group = h.groups.models.Group.get_by_pubid(public_group_id)

    user_id = urllib.unquote(request.matchdict["user"])

    annotations = annotran.groups.views.read_group(request, group, language=language, search_url=url,
                                                   user=user_id, render=False)

    ret = []
    originals = []

    for annotation in annotations:
        ret.append(annotation.annotation['text'])

        for selector in annotation.annotation['target'][0]['selector']:
            if 'exact' in selector:
                originals.append(selector['exact'])

    return {'annotations': ret,
            'full_annotations': annotations,
            'original': originals,
            'user': urllib.quote(user_id, safe=''),
            'pageId': urllib.quote(urllib.quote(url, safe=''), safe=''),
            'language': public_language_id,
            'group': public_group_id,
            'report': request.matchdict["report"]}


def includeme(config):
    """
    Pyramid includeme setup method to add routes
    :param config: the configuration supplied by pyramid
    :return: None
    """
    config.add_route('admin_reports', '/admin/reports')
    config.add_route('admin_view_translation', '/admin/view/translation/{page}/{group}/{language}/{user}/{report}')
    config.add_route('admin_delete_translation', '/admin/delete/translation/{page}/{group}/{language}/{user}/{report}')
    config.add_route('admin_delete_report', '/admin/delete/report/{page}/{group}/{language}/{user}/{report}')
    config.add_route('admin_delete_block_translation',
                     '/admin/delete/block/translation/{page}/{group}/{language}/{user}/{report}')
    config.add_route('admin_delete_block_report',
                     '/admin/delete/block/report/{page}/{group}/{language}/{user}/{report}')
    config.scan(__name__)

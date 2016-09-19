import urllib

import annotran
import h
from pyramid import view
from h import models
from h.api import search
from annotran.api.search import core as annotran_search
from pyramid import httpexceptions as exc
import annotran.reports.models
import annotran.pages.models
import h.accounts.models
import h.groups.models
import annotran.languages.models
import h.util


def delete_annotations(request, group, language=None, search_url=None, user=None):
    """Delete a set of annotations
    """

    if group is None:
        pubid = "__world__"
        slug = "Public"
    else:
        pubid = group.pubid
        slug = group.slug

    url = request.route_url('group_read', pubid=pubid, slug=slug)

    # language = models.Language.get_by_groupubid(group.pubid)

    parameters = {"group": pubid, "limit": 1000}

    if language:
        parameters['language'] = language.pubid

    if search_url:
        parameters['uri'] = search_url

    if user:
        parameters['user'] = user

    result = annotran_search.delete(request,
                                    private=True,
                                    params=parameters)


@view.view_config(route_name='admin_reports',
                  request_method='GET',
                  renderer='annotran:templates/admin/reports.html.jinja2',
                  permission='admin_reports')
def reports_index(_):
    reports = annotran.reports.models.Report.get_all()

    ret_list = []

    for report in reports:
        ret_dict = {}
        ret_dict["url"] = annotran.pages.models.Page.get_by_id(report.page_id).uri
        ret_dict["url_encoded"] = urllib.quote(urllib.quote(ret_dict["url"], safe=''), safe='')
        ret_dict["group"] = h.groups.models.Group.get_by_id(report.group_id).pubid
        ret_dict["language"] = annotran.languages.models.Language.get_by_id(report.language_id).pubid
        ret_dict["author"] = h.util.userid_from_username(
            h.accounts.models.User.query.filter(h.accounts.models.User.id == report.author_id).first().username,
            request=_)
        ret_dict["reporter"] = h.util.userid_from_username(
            h.accounts.models.User.query.filter(h.accounts.models.User.id == report.reporter_id).first().username,
            request=_)
        ret_dict["id"] = report.id

        ret_list.append(ret_dict)

    return {'reports': ret_list}


@view.view_config(route_name='admin_delete_report',
                  request_method='GET',
                  renderer='annotran:templates/admin/translation.html.jinja2',
                  permission='admin_delete_report')
def reports_delete_report(request):
    url = urllib.unquote(urllib.unquote(request.matchdict["page"]))
    page = annotran.pages.models.Page.get_by_uri(url)
    user = request.matchdict["user"]
    pubid = request.matchdict["language"]
    language = annotran.languages.models.Language.get_by_pubid(pubid, page)
    user_obj = h.accounts.models.User.query.filter(
        h.accounts.models.User.username == h.util.split_user(user)["username"]).first()

    groupubid = request.matchdict["group"]
    group = h.groups.models.Group.get_by_pubid(groupubid)

    delete_report(page, language, group, user_obj)

    return exc.HTTPSeeOther("/admin/reports")


@view.view_config(route_name='admin_delete_block_translation',
                  request_method='GET',
                  renderer='annotran:templates/admin/translation.html.jinja2',
                  permission='admin_delete_block_translation')
def reports_delete_block(request, block=False):
    return reports_delete(request, block=True)


@view.view_config(route_name='admin_delete_translation',
                  request_method='GET',
                  renderer='annotran:templates/admin/translation.html.jinja2',
                  permission='admin_delete_translation')
def reports_delete(request, block=False):
    url = urllib.unquote(urllib.unquote(request.matchdict["page"]))
    page = annotran.pages.models.Page.get_by_uri(url)
    user = request.matchdict["user"]
    pubid = request.matchdict["language"]
    language = annotran.languages.models.Language.get_by_pubid(pubid, page)
    user_obj = h.accounts.models.User.query.filter(
        h.accounts.models.User.username == h.util.split_user(user)["username"]).first()

    groupubid = request.matchdict["group"]
    group = h.groups.models.Group.get_by_pubid(groupubid)

    # load the annotations so that we can manipulate them
    initial_values = reports_view(request)

    annotations = initial_values['full_annotations']

    for annotation in annotations:
        # call elasticsearch to delete the record
        delete_annotations(request, group=group, language=language, search_url=url, user=user)

    delete_report(page, language, group, user_obj)

    if block:
        dummy_user = h.accounts.models.User.get_by_username("ADummyUserForGroupCreation")
        user_obj.activation_id = dummy_user.activation_id

        request.db.flush()

    return exc.HTTPSeeOther("/admin/reports")


def delete_report(page, language, group, user_obj):
    # NB this function deletes all reports pertaining to this translation
    annotran.reports.models.Report.query.filter(annotran.reports.models.Report.page == page,
                                                annotran.reports.models.Report.language == language,
                                                annotran.reports.models.Report.group == group,
                                                annotran.reports.models.Report.author == user_obj).delete()


@view.view_config(route_name='admin_view_translation',
                  request_method='GET',
                  renderer='annotran:templates/admin/translation.html.jinja2',
                  permission='admin_view_translation')
def reports_view(request):
    url = urllib.unquote(urllib.unquote(request.matchdict["page"]))
    page = annotran.pages.models.Page.get_by_uri(url)

    pubid = request.matchdict["language"]
    language = annotran.languages.models.Language.get_by_pubid(pubid, page)

    groupubid = request.matchdict["group"]
    group = h.groups.models.Group.get_by_pubid(groupubid)

    annotations = {}

    user = urllib.unquote(request.matchdict["user"])

    annotations = h.groups.views._read_group(request, group, language=language, search_url=url, user=user, render=False)

    ret = []
    originals = []

    for annotation in annotations:
        ret.append(annotation.annotation['text'])

        try:
            for selector in annotation.annotation['target'][0]['selector']:
                if 'exact' in selector:
                    originals.append(selector['exact'])
        except:
            originals.append("No linking text found")

    return {'annotations': ret,
            'full_annotations': annotations,
            'original': originals,
            'user': urllib.quote(user, safe=''),
            'pageId': urllib.quote(urllib.quote(url, safe=''), safe=''),
            'language': pubid,
            'group': groupubid,
            'report': request.matchdict["report"]}


def includeme(config):
    config.add_route('admin_reports', '/admin/reports')
    config.add_route('admin_view_translation', '/admin/view/translation/{page}/{group}/{language}/{user}/{report}')
    config.add_route('admin_delete_translation', '/admin/delete/translation/{page}/{group}/{language}/{user}/{report}')
    config.add_route('admin_delete_report', '/admin/delete/report/{page}/{group}/{language}/{user}/{report}')
    config.add_route('admin_delete_block_translation',
                     '/admin/delete/block/translation/{page}/{group}/{language}/{user}/{report}')
    config.scan(__name__)

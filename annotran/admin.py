import urllib

import annotran
import h
from pyramid import view
from h import models
from h.api import search
from annotran.api.search import core as annotran_search
from pyramid import httpexceptions as exc


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
    return {}


@view.view_config(route_name='admin_delete_translation',
                  request_method='GET',
                  renderer='annotran:templates/admin/translation.html.jinja2',
                  permission='admin_delete_translation')
def reports_delete(request):
    url = urllib.unquote(urllib.unquote(request.matchdict["page"]))
    page = annotran.pages.models.Page.get_by_uri(url)
    user = request.matchdict["user"]
    pubid = request.matchdict["language"]
    language = annotran.languages.models.Language.get_by_pubid(pubid, page)

    groupubid = request.matchdict["group"]
    group = h.groups.models.Group.get_by_pubid(groupubid)

    # load the annotations so that we can manipulate them
    initial_values = reports_view(request)

    annotations = initial_values['full_annotations']

    for annotation in annotations:
        # call elasticsearch to delete the record
        delete_annotations(request, group=group, language=language, search_url=url, user=user)

    return exc.HTTPSeeOther("/admin/reports")


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
    config.scan(__name__)

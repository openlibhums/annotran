import urllib

import annotran
import h
from pyramid import view
from h import models


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
    user = request.matchdict["user"]

    # load the annotations so that we can manipulate them
    initial_values = reports_view(request)

    annotations = initial_values['full_annotations']

    for annotation in annotations:
        if (annotation.href == url or annotation.href == url + "/") and (
            annotation.annotation['user'][5:].split("@")[0] == user):
                # call elasticsearch to delete the record
                pass


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

    user =  urllib.unquote(request.matchdict["user"])

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
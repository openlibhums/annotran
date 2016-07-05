'''

Copyright (c) 2013-2014 Hypothes.is Project and contributors

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

#this is a code reused from hypothesis, adapted and extended to be used for languages

# -*- coding: utf-8 -*-

import collections

import deform
from pyramid import httpexceptions as exc
from pyramid.view import view_config
from pyramid import renderers


from h import i18n
import models
from h import presenters
from h.api import search
from h.api import uri
from annotran.languages import schemas
import h
import annotran

_ = i18n.TranslationString




@view_config(route_name='language_add',
             request_method='POST')
def addLanguage(request):
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    language = request.matchdict["language"]
    groupubid = request.matchdict["groupubid"]

    language = models.Language(name=language, group = h.groups.models.Group.get_by_pubid(groupubid))
    request.db.add(language)

    # We need to flush the db session here so that language.id will be generated.
    request.db.flush()

    url = request.route_url('language_read', pubid=language.pubid, groupubid=groupubid)
    return exc.HTTPSeeOther(url)



@view_config(route_name='language_read', request_method='GET')
def read(request):
    pubid = request.matchdict["pubid"]
    groupubid = request.matchdict["groupubid"]
    language = models.Language.get_by_pubid(pubid)
    group = h.groups.models.Group.get_by_pubid(groupubid)
    if group is None:
        raise exc.HTTPNotFound()
    if not request.authenticated_userid:
        return None
    else:
        if group in request.authenticated_user.groups:
            return _read_group(request, group, language)
        else:
            return None

def _read_group(request, group, language):
    """Return the rendered "Share this group" page.

    This is the page that's shown when a user who is already a member of a
    group visits the group's URL.

    """
    url = request.route_url('group_read', pubid=group.pubid, slug=group.slug)


    #language = models.Language.get_by_groupubid(group.pubid)

    '''
    result = search.search(request,
                           private=False,
                           params={"group": group.pubid, "limit": 1000})
    annotations = [presenters.AnnotationHTMLPresenter(models.Annotation(a))
                   for a in result['rows']]

    # Group the annotations by URI.
    # Create a dict mapping the (normalized) URIs of the annotated documents
    # to the most recent annotation of each document.
    annotations_by_uri = collections.OrderedDict()
    for annotation in annotations:
        normalized_uri = uri.normalize(annotation.uri)
        if normalized_uri not in annotations_by_uri:
            annotations_by_uri[normalized_uri] = annotation
            if len(annotations_by_uri) >= 25:
                break

    document_links = [annotation.document_link
                      for annotation in annotations_by_uri.values()]

    template_data = {
        'group': group, 'group_url': url, 'document_links': document_links}

    return renderers.render_to_response(
        renderer_name='h:templates/groups/share.html.jinja2',
        value=template_data, request=request)
    '''

def includeme(config):
    config.add_route('language_add', 'languages/{language}/{groupubid}/addLanguage')
    config.add_route('language_read', '/languages/{pubid}/{groupubid}')
    config.scan(__name__)

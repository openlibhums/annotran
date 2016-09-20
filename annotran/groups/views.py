"""
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
"""
# monkey patching of hypothesis methods

# annotran's version of h.groups.views._read_group
import collections

import h
from h import presenters
from h.api import search
from h.api import uri
from pyramid import renderers
import h.models


def read_group(request, group, language=None, search_url=None, user=None, render=True):
    """
    Return the rendered "Share this group" page.

    This is the page that's shown when a user who is already a member of a group visits the group's URL.
    :param request: a request object
    :param group: a group object
    :param language: a language object to search or None
    :param search_url: the URL to search or None
    :param user: the user object to search or None
    :param render: whether or not to return a context object
    :return: if render, a context object for a template. If render is false, a list of annotations
    """

    if group is None:
        public_group_id = "__world__"
        slug = "Public"
    else:
        public_group_id = group.pubid
        slug = group.slug

    url = request.route_url('group_read', pubid=public_group_id, slug=slug)

    parameters = {"group": public_group_id, "limit": 1000}

    if language:
        parameters['language'] = language.pubid

    if search_url:
        parameters['uri'] = search_url

    if user:
        parameters['user'] = user

    result = search.search(request,
                           private=False,
                           params=parameters)

    annotations = [presenters.AnnotationHTMLPresenter(h.models.Annotation(a))
                   for a in result['rows']]

    if render:
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
    else:
        return annotations

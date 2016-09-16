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
# monkey patching of hypothesis methods

# annotran's version of h.groups.views._read_group
import collections

import h
from h import presenters
from h.api import search
from h.api import uri
from pyramid import renderers

class Views:

    @staticmethod
    def _read_group(request, group, language=None, render=True):
        """Return the rendered "Share this group" page.

        This is the page that's shown when a user who is already a member of a
        group visits the group's URL.

        """

        if group is None:
            pubid = "__world__"
            slug = "Public"
        else:
            pubid = group.pubid
            slug = group.slug

        url = request.route_url('group_read', pubid=pubid, slug=slug)

        # language = models.Language.get_by_groupubid(group.pubid)

        result = search.search(request,
                               private=False,
                               params={"group": pubid, "limit": 1000})
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

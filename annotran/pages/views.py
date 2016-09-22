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

# -*- coding: utf-8 -*-
import urllib

import annotran
import annotran.languages.models
import models
from h import i18n
from pyramid import httpexceptions as exc
from pyramid.view import view_config

_ = i18n.TranslationString


@view_config(route_name='page_add',
             request_method='POST')
def add_page(request):
    """
    Add a page to the database
    :param request: a request object
    :return: a redirect to the language_read URL
    """
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    name = request.matchdict["language_name"]
    page_id = urllib.unquote(urllib.unquote(request.matchdict["page_url"]))
    public_group_id = request.matchdict["public_group_id"]

    language = annotran.languages.models.Language.get_by_name(name)
    page = annotran.pages.models.Page.get_by_uri(page_id)

    if not page:
        page = annotran.pages.models.Page(uri=page_id, language=language)
        request.db.add(page)
    else:
        page.members.append(language)
    request.db.flush()

    url = request.route_url('language_read', public_language_id=language.pubid, public_group_id=public_group_id)
    return exc.HTTPSeeOther(url)


def includeme(config):
    """
    Pyramid's router configuration
    :param config: the config object to which to append routes
    :return: None
    """
    config.add_route('page_add', 'pages/{language_name}/{page_url}/{public_group_id}/addPage')
    config.scan(__name__)

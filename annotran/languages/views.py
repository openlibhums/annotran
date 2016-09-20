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
from pyramid import httpexceptions as exc
from pyramid.view import view_config
from h import i18n
from annotran.util import util

import models
import h
import annotran
import h.groups.models
import annotran.pages.models
import annotran.groups.views

_ = i18n.TranslationString


@view_config(route_name='language_add',
             request_method='POST')
def add_language(request):
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    name = request.matchdict["language"]
    public_group_id = request.matchdict["public_group_id"]

    group = h.groups.models.Group.get_by_pubid(public_group_id)
    language = models.Language.get_by_name(name)

    if not language:
        if group:
            language = models.Language(name=name, group=group)
        else:
            language = models.Language(name=name)
        request.db.add(language)
    else:
        if group:
            language.members.append(group)
    # We need to flush the db session here so that language.id will be generated.
    request.db.flush()
    url = request.route_url('language_read', public_language_id=language.pubid, public_group_id=public_group_id)
    return exc.HTTPSeeOther(url)


@view_config(route_name='language_read', request_method='GET')
def read(request):
    url=util.get_url_from_request(request)

    page = annotran.pages.models.Page.get_by_uri(url)
    pubid = request.matchdict["public_language_id"]
    language = models.Language.get_by_public_language_id(pubid, page)
    groupubid = request.matchdict["public_group_id"]
    group = h.groups.models.Group.get_by_pubid(groupubid)

    if group.id == -1:
        # this is the public group
        return annotran.groups.views.read_group(request, group, language=language)
    if not request.authenticated_userid:
        return None
    else:
        if group in request.authenticated_user.groups:
            return annotran.groups.views.read_group(request, group, language=language)
        else:
            return None

def includeme(config):
    config.add_route('language_add', 'languages/{language}/{public_group_id}/{page_id}/addLanguage')
    config.add_route('language_read', '/languages/{public_language_id}/{public_group_id}')
    config.scan(__name__)

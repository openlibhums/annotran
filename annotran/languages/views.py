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
from annotran import replacements

_ = i18n.TranslationString




@view_config(route_name='language_add',
             request_method='POST')
def addLanguage(request):
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    language = request.matchdict["language"]
    groupubid = request.matchdict["groupubid"]
    group = h.groups.models.Group.get_by_pubid(groupubid)

    if group:
        language = models.Language(name=language, group=h.groups.models.Group.get_by_pubid(groupubid))
    else:
        language = models.Language(name=language)

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
        # this is the public group
        return replacements._read_group(request, group, language)
    if not request.authenticated_userid:
        return None
    else:
        if group in request.authenticated_user.groups:
            return replacements._read_group(request, group, language)
        else:
            return None




def includeme(config):
    config.add_route('language_add', 'languages/{language}/{groupubid}/addLanguage')
    config.add_route('language_read', '/languages/{pubid}/{groupubid}')
    config.scan(__name__)

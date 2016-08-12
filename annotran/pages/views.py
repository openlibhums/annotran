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

from pyramid import httpexceptions as exc
from pyramid.view import view_config
from h import i18n

import models
import annotran


_ = i18n.TranslationString


@view_config(route_name='page_add',
             request_method='POST')
def addPage(request):
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    name = request.matchdict["languageName"]
    pageid = request.matchdict["pageId"]
    groupubid = request.matchdict["groupubid"]

    language = annotran.languages.models.Language.get_by_name(name)

    page = annotran.pages.models.Page.get_by_uri(pageid)
    if not page:
        page = annotran.pages.models.Page(uri = pageid, language = language)
        request.db.add(page)
        request.db.flush()
    else:
        page.members.append(language)

    url = request.route_url('language_read', pubid=language.pubid, groupubid=groupubid)
    return exc.HTTPSeeOther(url)

def includeme(config):
    config.add_route('page_add', 'pages/{languageName}/{pageId}/{groupubid}/addPage')
    config.scan(__name__)

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

import models

_ = i18n.TranslationString


@view_config(route_name='language_add',
             request_method='POST')
def add_language(request):
    """
    This view adds a language
    :param request: a request object
    :return: None
    """
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    name = request.matchdict["language"]
    public_group_id = request.matchdict["public_group_id"]

    language = models.Language.get_by_name(name)

    if not language:
        language = models.Language(name=name)
        request.db.add(language)
        # We need to flush the db session here so that language.id will be generated.
        request.db.flush()
    url = request.route_url('translation_read', public_language_id=language.pubid, public_group_id=public_group_id)
    return exc.HTTPSeeOther(url)

def includeme(config):
    """
    Pyramid's router configuration
    :param config: the config to which to commit the routes
    :return: None
    """
    config.add_route('language_add', 'languages/{language}/{public_group_id}/addLanguage')
    config.scan(__name__)

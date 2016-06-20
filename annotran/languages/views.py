# -*- coding: utf-8 -*-

import collections

import deform
from pyramid import httpexceptions as exc
from pyramid.view import view_config
from pyramid import renderers


from h import i18n
import models
from annotran.languages import schemas

import annotran.session


_ = i18n.TranslationString



@view_config(route_name='language_add',
             request_method='POST')
def addLanguage(request):
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    language = models.Language(
        name='EN_language', creator=request.authenticated_user)
    request.db.add(language)

    # We need to flush the db session here so that language.id will be generated.
    request.db.flush()

    #url = request.route_url('language_read', pubid=language.pubid, slug=language.slug)
    return exc.HTTPSeeOther(url)


def includeme(config):
    config.add_route('language_add', '/languages/addLanguage')
    config.scan(__name__)


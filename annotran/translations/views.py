# -*- coding: utf-8 -*-
import urllib

from pyramid import httpexceptions as exc
from pyramid.view import view_config
from h import i18n
from annotran.util import util

import h
import annotran
import h.groups.models
import annotran.pages.models
import annotran.groups.views

from annotran.languages.models import Language as lang_models
from annotran.translations.models import Translation as tran_models

_ = i18n.TranslationString


@view_config(route_name='add_translation',
             request_method='POST')
def add_translation(request):
    """
    This view adds a translation
    :param request: a request object
    :return: a redirect to the translation_read method

    """
    if request.authenticated_userid is None:
        raise exc.HTTPNotFound()

    name = request.matchdict["language"]
    public_group_id = request.matchdict["public_group_id"]
    page_url = urllib.unquote(urllib.unquote(request.matchdict["page_url"]))
    page = annotran.pages.models.Page.get_by_uri(page_url)

    group = h.groups.models.Group.get_by_pubid(public_group_id)
    language = annotran.languages.models.Language.get_by_name(name)

    translation = None
    if page and language and group:
        translation = annotran.translations.models.Translation.get_by_composite_id(page.id, language.id, group.id)
    else:
        return {}

    if translation is None:
        translation = annotran.translations.models.Translation(page=page, language=language, group=group)
        request.db.add(translation)
        request.db.flush()

    url = request.route_url('translation_read', public_language_id=language.pubid, public_group_id=public_group_id)
    return exc.HTTPSeeOther(url)


@view_config(route_name='translation_read', request_method='GET')
def read(request):
    """
    Read the list of languages available in a group
    :param request: the request object
    :return: a list of languages in a group
    """
    url = util.get_url_from_request(request)

    page = annotran.pages.models.Page.get_by_uri(url)
    public_language_id = request.matchdict["public_language_id"]
    language = lang_models.get_by_public_language_id(public_language_id)
    public_group_id = request.matchdict["public_group_id"]
    group = h.groups.models.Group.get_by_pubid(public_group_id)

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
    """
    Pyramid's router configuration
    :param config: the config to which to commit the routes
    :return: None
    """
    config.add_route('add_translation', 'translations/{language}/{public_group_id}/{page_url}/addTranslation')
    config.add_route('translation_read', '/languages/{public_language_id}/{public_group_id}')
    config.scan(__name__)
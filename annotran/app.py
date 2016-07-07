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

#a lot of code here has been reused from hypothesis

import collections

from pyramid.config import Configurator
from pyramid import renderers
from pyramid import httpexceptions as exc

from jinja2 import Environment, PackageLoader

import h.app
import h.client
from h.assets import *
from h.config import settings_from_environment

from annotran import languages



def includeme(config):
    config.registry.settings.setdefault('webassets.bundles', 'annotran:assets.yaml')
    config.include('pyramid_webassets')
    config.override_asset(
        to_override='h:templates/old-home.html.jinja2',
        override_with='annotran:templates/home.html.jinja2')
    config.override_asset(
        to_override='h:templates/client/top_bar.html',
        override_with='annotran:templates/client/top_bar.html')
    config.override_asset(
        to_override='h:templates/app.html.jinja2',
        override_with='annotran:templates/app.html.jinja2')
    #config.add_webasset()
    config.commit()

def get_settings(global_config, **settings):
    result = {}
    result.update(settings)
    result.update(settings_from_environment())
    return result


def main(global_config, **settings):
    settings = get_settings(global_config, **settings)
    config = Configurator(settings=settings)

    #add settings from H to init H from annotran
    config.set_root_factory('h.resources.create_root')
    config.add_subscriber('h.subscribers.add_renderer_globals',
                      'pyramid.events.BeforeRender')
    config.add_subscriber('h.subscribers.publish_annotation_event',
                      'h.api.events.AnnotationEvent')
    config.add_tween('h.tweens.conditional_http_tween_factory', under='pyramid.tweens.excview_tween_factory')
    config.add_tween('h.tweens.csrf_tween_factory')
    config.add_tween('h.tweens.auth_token')
    config.add_renderer('csv', 'h.renderers.CSV')
    config.include('h.app')
    config.scan('h.client')
    config.include('annotran.languages')
    config.include(__name__)

    #overwritten functions from h
    h.client.ANGULAR_DIRECTIVE_TEMPLATES.insert(4, 'language_list')
    h.client.ANGULAR_DIRECTIVE_TEMPLATES.insert(5, 'user_list')
    h.client.ANGULAR_DIRECTIVE_TEMPLATES.insert(6, 'top_bar')
    h.client._angular_template_context = _angular_template_context_ext
    h.session.model = model
    h.groups.views._read_group = languages.views._read_group
    return config.make_wsgi_app()

def _angular_template_context_ext(name):
    """Return the context for rendering a 'text/ng-template' <script>
       tag for an Angular directive.
    """
    jinja_env_ext = Environment(loader=PackageLoader(__package__, 'templates'))
    jinja_env = h.client.jinja_env
    if (name == 'user_list' or name == 'language_list' or name == 'top_bar'):
        angular_template_path = 'client/{}.html'.format(name)
        content, _, _ = jinja_env_ext.loader.get_source(jinja_env_ext,
                                                    angular_template_path)
    else:
        angular_template_path = 'client/{}.html'.format(name)
        content, _, _ = jinja_env.loader.get_source(jinja_env,
                                                angular_template_path)
    return {'name': '{}.html'.format(name), 'content': content}


def model(request):
    session = {}
    session['csrf'] = request.session.get_csrf_token()
    session['userid'] = request.authenticated_userid
    session['groups'] = h.session._current_groups(request)
    session['features'] = h.session.features.all(request)
    session['languages'] = _current_languages(request)
    session['preferences'] = {}
    user = request.authenticated_user
    if user and not user.sidebar_tutorial_dismissed:
        session['preferences']['show_sidebar_tutorial'] = True
    return session

def _language_sort_key(language):
    """Sort private languages for the session model list"""

    # languages are sorted first by name but also by ID
    # so that multiple languages with the same name are displayed
    # in a consistent order in clients
    return (language.name.lower(), language.pubid)

def _current_languages(request):
    """Return a list of the groups the current user is a member of.

    This list is meant to be returned to the client in the "session" model.

    """
    '''
        if groupubid is None:
        group = {'name': 'Public', 'id': '__world__', 'public': True}
        return None
    else:
        group = h.groups.models.Group.get_by_pubid(groupubid)
    '''

    languages = []
    userid = request.authenticated_userid
    if userid is None:
        return languages
    user = request.authenticated_user
    # if user is None or get_group(request) is None:
    #   return languages
    # return languages for all groups for that particular user
    for group in user.groups:
        for language in group.languages:
            languages.append({
                'groupubid': group.pubid,
                'name': language.name,
                'id': language.pubid,
                'url': request.route_url('language_read',
                                         pubid=language.pubid, groupubid=group.pubid),
            })

    return languages

def get_group(request):
    if request.matchdict.get('pubid') is None:
        return None
    pubid = request.matchdict["pubid"]
    group = h.groups.models.Group.get_by_pubid(pubid)
    if group is None:
        raise exc.HTTPNotFound()
    return group

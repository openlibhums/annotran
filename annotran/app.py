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

import annotran
import annotran.api.search.query
import annotran.mailer
import annotran.resources
import annotran.views
import h.accounts.views
import h.api.groups
import h.api.search.query
import h.app
import h.assets
import h.client
import h.config
import h.groups
import h.groups.views
import h.mailer
import h.resources
import h.session
import h.views
import pyramid.events
from annotran import client
from annotran import session
from annotran.accounts import views as accounts_views
from annotran.groups import views as groups_views
from h.config import settings_from_environment
from pyramid.config import Configurator


def includeme_override(config):
    """
    Pyramid includeme definition for override. This does nothing but stops Pyramid from doing its own thing.
    :param config: a Pyramid configuration object to which overrides will be committed
    :return: None
    """
    pass


def get_settings(**settings):
    """
    Load settings from Pyramid startup into a dictionary
    :param settings: the settings dictionary to evaluate
    :return: a result
    """
    result = {}
    result.update(settings)
    result.update(settings_from_environment())
    return result


def main(global_config, **settings):
    """
    The main Pyramid entry point
    :param global_config: a global configuration option as required by Pyramid's specification
    :param settings: a dictionary of arbitrary key/value pairs, read from Pyramid's configuration
    :return: a WSGI app
    """
    h.assets.includeme = includeme_override
    settings = get_settings(**settings)
    config = Configurator(settings=settings)

    # add settings from H to init H from annotran
    config.set_root_factory('h.resources.create_root')
    config.add_subscriber('h.subscribers.add_renderer_globals', 'pyramid.events.BeforeRender')
    config.add_subscriber('h.subscribers.publish_annotation_event', 'h.api.events.AnnotationEvent')
    config.add_tween('h.tweens.conditional_http_tween_factory', under='pyramid.tweens.excview_tween_factory')
    config.add_tween('h.tweens.csrf_tween_factory')
    config.add_tween('h.tweens.auth_token')
    config.add_renderer('csv', 'h.renderers.CSV')
    config.include('h.app')
    config.scan('h.client')
    config.include('annotran.languages')
    config.include('annotran.pages')
    config.include('annotran.votes')
    config.include('annotran.admin')
    config.include('annotran.reports')
    config.include('annotran.help')

    config.add_subscriber_predicate('asset_request', h.assets.AssetRequest)
    config.add_subscriber(h.assets.asset_response_subscriber, pyramid.events.NewResponse, asset_request=True)
    config.registry.settings.setdefault('webassets.bundles', 'annotran:assets.yaml')
    config.include('pyramid_webassets')
    config.override_asset(to_override='h:templates/old-home.html.jinja2',
                          override_with='annotran:templates/home.html.jinja2')
    config.override_asset(to_override='h:templates/includes/logo-header.html.jinja2',
                          override_with='annotran:templates/includes/logo-header.html.jinja2')
    config.override_asset(to_override='h:templates/accounts/profile.html.jinja2',
                          override_with='annotran:templates/accounts/profile.html.jinja2')
    config.override_asset(to_override='h:templates/notfound.html.jinja2',
                          override_with='annotran:templates/notfound.html.jinja2')
    config.override_asset(to_override='h:templates/5xx.html.jinja2',
                          override_with='annotran:templates/5xx.html.jinja2')
    config.override_asset(to_override='h:templates/layouts/admin.html.jinja2',
                          override_with='annotran:templates/layouts/admin.html.jinja2')
    config.override_asset(to_override='h:templates/admin/index.html.jinja2',
                          override_with='annotran:templates/admin/index.html.jinja2')
    config.override_asset(to_override='h:templates/groups/share.html.jinja2',
                          override_with='annotran:templates/groups/share.html.jinja2')
    config.override_asset(to_override='h:templates/groups/about-groups.html.jinja2',
                          override_with='annotran:templates/groups/about-groups.html.jinja2')
    config.commit()

    config.add_static_view(name='annotran_images', path='static/images')

    # it is necessary to add *new* angular directives here but not those that are being overridden
    h.client.ANGULAR_DIRECTIVE_TEMPLATES.append('language_list')
    h.client.ANGULAR_DIRECTIVE_TEMPLATES.append('user_list')

    # the following functions are monkey-patched inside H in order to give the annotran context
    h.client._angular_template_context = client.angular_template_context
    h.client.render_app_html = client.render_app_html
    h.client._app_html_context = client.app_html_context

    h.session.model = session.model

    h.mailer.send = annotran.mailer.send

    h.groups.views.read_group = groups_views.read_group

    h.accounts.views.ProfileController.get = accounts_views.ProfileController.profile_get

    h.views.error = annotran.views.error
    h.views.json_error = annotran.views.json_error

    h.resources.Root.__acl__ = annotran.resources.__acl__

    h.api.search.query.Builder.build = annotran.api.search.query.build

    # load the support email address
    annotran.views.Shared.support_address = settings.get('annotran.app.support_address')
    return config.make_wsgi_app()

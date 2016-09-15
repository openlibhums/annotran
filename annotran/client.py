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

import json
import os
from urlparse import urlparse

import annotran.views
import h
from h import __version__
from jinja2 import Environment, PackageLoader

jinja_env = Environment(loader=PackageLoader(__package__, 'templates'))


jinja_env = Environment(loader=PackageLoader(__package__, 'templates'))


# annotran's version of h.client._angular_template_context
def _angular_template_context_ext(name):
    """Return the context for rendering a 'text/ng-template' <script>
       tag for an Angular directive.
    """
    jinja_env_ext = Environment(loader=PackageLoader(__package__, 'templates'))
    jinja_env = h.client.jinja_env

    # first look if there is a local copy in annotran that we should use
    angular_template_path = 'client/{}.html'.format(name)
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    if os.path.isfile('{0}/templates/{1}'.format(BASE_DIR, angular_template_path)):
        content, _, _ = jinja_env_ext.loader.get_source(jinja_env_ext,
                                                        angular_template_path)
    else:
        content, _, _ = jinja_env.loader.get_source(jinja_env,
                                                    angular_template_path)
    return {'name': '{}.html'.format(name), 'content': content}


def _app_html_context(webassets_env, api_url, service_url, ga_tracking_id, sentry_public_dsn, websocket_url):
    """
    Returns a dict of asset URLs and contents used by the sidebar app
    HTML tempate.
    """

    if urlparse(service_url).hostname == 'localhost':
        ga_cookie_domain = 'none'
    else:
        ga_cookie_domain = 'auto'

    # the serviceUrl parameter must contain a path element
    service_url = h.client.url_with_path(service_url)

    app_config = {
        'apiUrl': api_url,
        'serviceUrl': service_url,
        'supportAddress': annotran.views.Shared.support_address
    }

    if websocket_url:
        app_config.update({
            'websocketUrl': websocket_url,
        })

    if sentry_public_dsn:
        app_config.update({
            'raven': {
                'dsn': sentry_public_dsn,
                'release': __version__
            }
        })

    return {
        'app_config': json.dumps(app_config),
        'angular_templates': map(h.client._angular_template_context,
                                 h.client.ANGULAR_DIRECTIVE_TEMPLATES),
        'app_css_urls': h.client.asset_urls(webassets_env, 'app_css'),
        'app_js_urls': h.client.asset_urls(webassets_env, 'app_js'),
        'ga_tracking_id': ga_tracking_id,
        'ga_cookie_domain': ga_cookie_domain,
        'register_url': service_url + 'register',
    }


# h.client.render_app_html
def render_app_html(webassets_env,
                    service_url,
                    api_url,
                    sentry_public_dsn,
                    ga_tracking_id=None,
                    websocket_url=None,
                    extra={}):
    template = jinja_env.get_template('app.html.jinja2')
    assets_dict = h.client._app_html_context(api_url=api_url,
                                             service_url=service_url,
                                             ga_tracking_id=ga_tracking_id,
                                             sentry_public_dsn=sentry_public_dsn,
                                             webassets_env=webassets_env,
                                             websocket_url=websocket_url)
    return template.render(h.client._merge(assets_dict, extra))

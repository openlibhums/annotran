from pyramid.config import Configurator

from h.assets import *

from h.config import settings_from_environment
from jinja2 import Environment, PackageLoader

import h.app
import h.client
from h.client import ANGULAR_DIRECTIVE_TEMPLATES


def includeme(config):
    config.registry.settings.setdefault('webassets.bundles', 'annotran:assets.yaml')
    config.include('pyramid_webassets')
    config.override_asset(
        to_override='h:templates/old-home.html.jinja2',
        override_with='annotran:templates/home.html.jinja2')
    config.override_asset(
        to_override='h:templates/client/top_bar.html',
        override_with='annotran:templates/client/top_bar.html')
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
    config.include(__name__)
    config.include('h.app')
    config.scan('h.client')

    h.client.ANGULAR_DIRECTIVE_TEMPLATES.insert(4, 'language_list')
    h.client._angular_template_context = _angular_template_context_ext
    return config.make_wsgi_app()

def _angular_template_context_ext(name):
    """Return the context for rendering a 'text/ng-template' <script>
       tag for an Angular directive.
    """
    jinja_env_ext = Environment(loader=PackageLoader(__package__, 'templates'))
    jinja_env = h.client.jinja_env
    if (name == 'language_list' or name == 'top_bar'):
        angular_template_path = 'client/{}.html'.format(name)
        content, _, _ = jinja_env_ext.loader.get_source(jinja_env_ext,
                                                    angular_template_path)
    else:
        angular_template_path = 'client/{}.html'.format(name)
        content, _, _ = jinja_env.loader.get_source(jinja_env,
                                                angular_template_path)
    return {'name': '{}.html'.format(name), 'content': content}


def configure_jinja2_assets(config):
    assets_env = config.get_webassets_env()
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.assets_environment = assets_env
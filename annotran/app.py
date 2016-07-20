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
import h.config
from h.assets import *
from h.config import settings_from_environment

from annotran import replacements
from annotran import languages

import json






def includeme(config):
    config.registry.settings.setdefault('webassets.bundles', 'annotran:assets.yaml')
    config.include('pyramid_webassets')
    config.override_asset(to_override = 'h:templates/old-home.html.jinja2',
                        override_with = 'annotran:templates/home.html.jinja2')
    config.commit()


def get_settings(global_config, **settings):
    result = {}
    result.update(settings)
    result.update(settings_from_environment())
    return result


def main(global_config, **settings):
    h.assets.includeme = override_hypothesis_includeme
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

    config.add_static_view(name='annotran_images', path='static/images')

    # it is necessary to add *new* angular directives here but not those that are being overridden
    h.client.ANGULAR_DIRECTIVE_TEMPLATES.append('language_list')
    h.client.ANGULAR_DIRECTIVE_TEMPLATES.append('user_list')
    h.client.ANGULAR_DIRECTIVE_TEMPLATES.append('top_bar')

    # the following functions are monkey-patched inside H in order to give the annotran context
    h.client._angular_template_context = replacements._angular_template_context_ext
    h.session.model = replacements.model
    h.groups.views._read_group = replacements._read_group
    h.api.groups.set_group_if_reply = replacements.set_group_if_reply
    h.client.render_app_html = replacements.render_app_html
    #h.api.search.query.GroupFilter = replacements.GroupFilter

    #ANNOTATION_MAPPING_EXT = json.loads(h.config.ANNOTATION_MAPPING)
    h.config.ANNOTATION_MAPPING = ANNOTATION_MAPPING_EXT
    return config.make_wsgi_app()


def override_hypothesis_includeme(config):
    # this method is an override of hypothes.is's default includeme. It fires instead and handles CORS.k
    config.add_subscriber_predicate('asset_request', AssetRequest)
    config.add_subscriber(
        asset_response_subscriber,
        pyramid.events.NewResponse,
        asset_request=True
    )

#TODO - rewrite this in a way that json is just extended and not the entire one is copied
ANNOTATION_MAPPING_EXT = {
    '_id': {'path': 'id'},
    '_source': {'excludes': ['id']},
    'analyzer': 'keyword',
    'properties': {
        'annotator_schema_version': {'type': 'string'},
        'created': {'type': 'date'},
        'updated': {'type': 'date'},
        'quote': {'type': 'string', 'analyzer': 'uni_normalizer'},
        'tags': {'type': 'string', 'analyzer': 'uni_normalizer'},
        'text': {'type': 'string', 'analyzer': 'uni_normalizer'},
        'deleted': {'type': 'boolean'},
        'uri': {
            'type': 'string',
            'index_analyzer': 'uri',
            'search_analyzer': 'uri',
            'fields': {
                'parts': {
                    'type': 'string',
                    'index_analyzer': 'uri_parts',
                    'search_analyzer': 'uri_parts',
                },
            },
        },
        'user': {'type': 'string', 'index': 'analyzed', 'analyzer': 'user'},
        'target': {
            'properties': {
                'source': {
                    'type': 'string',
                    'index_analyzer': 'uri',
                    'search_analyzer': 'uri',
                    'copy_to': ['uri'],
                },
                # We store the 'scope' unanalyzed and only do term filters
                # against this field.
                'scope': {
                    'type': 'string',
                    'index': 'not_analyzed',
                },
                'selector': {
                    'properties': {
                        'type': {'type': 'string', 'index': 'no'},

                        # Annotator XPath+offset selector
                        'startContainer': {'type': 'string', 'index': 'no'},
                        'startOffset': {'type': 'long', 'index': 'no'},
                        'endContainer': {'type': 'string', 'index': 'no'},
                        'endOffset': {'type': 'long', 'index': 'no'},

                        # Open Annotation TextQuoteSelector
                        'exact': {
                            'path': 'just_name',
                            'type': 'string',
                            'fields': {
                                'quote': {
                                    'type': 'string',
                                    'analyzer': 'uni_normalizer',
                                },
                            },
                        },
                        'prefix': {'type': 'string'},
                        'suffix': {'type': 'string'},

                        # Open Annotation (Data|Text)PositionSelector
                        'start': {'type': 'long'},
                        'end':   {'type': 'long'},
                    }
                }
            }
        },
        'permissions': {
            'index_name': 'permission',
            'properties': {
                'read': {'type': 'string'},
                'update': {'type': 'string'},
                'delete': {'type': 'string'},
                'admin': {'type': 'string'}
            }
        },
        'references': {'type': 'string'},
        'document': {
            'enabled': False,  # indexed explicitly by the save function
        },
        'thread': {
            'type': 'string',
            'analyzer': 'thread'
        },
        'group': {
            'type': 'string',
        },
        'language': {
            'type': 'string',
        }
    }
}
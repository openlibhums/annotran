from h import i18n
from pyramid.view import (view_config)

_ = i18n.TranslationStringFactory(__package__)


@view_config(route_name='termsofservice', request_method='GET',
             renderer='annotran:templates/terms-of-service.html.jinja2')
def terms_of_service(context, request):
    """Display the terms of service."""
    return {'support_address': Shared.support_address}


@view_config(route_name='communityguidelines', request_method='GET',
             renderer='annotran:templates/community-guidelines.html.jinja2')
def community_guidelines(context, request):
    """Display the terms of service."""
    return {'support_address': Shared.support_address}


@view_config(route_name='privacypolicy', request_method='GET',
             renderer='annotran:templates/privacy-policy.html.jinja2')
def privacy_policy(context, request):
    """Display the terms of service."""
    return {'support_address': Shared.support_address}


def includeme(config):
    """
    Pyramid includeme setup method to add routes
    :param config: the configuration supplied by pyramid
    :return: None
    """
    config.add_route('termsofservice', '/terms-of-service')
    config.add_route('communityguidelines', '/community-guidelines')
    config.add_route('privacypolicy', '/privacy-policy')
    config.scan(__name__)


class Shared(object):
    def __init__(self):
        pass

    support_address = ""

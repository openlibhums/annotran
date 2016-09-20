from pyramid.view import view_config


@view_config(renderer='annotran:templates/annotran_help.html.jinja2', route_name='annotran_help')
@view_config(renderer='annotran:templates/annotran_help.html.jinja2', route_name='annotran_onboarding')
def help_page(request):
    """
    Render the help page for annotran
    :param request: the current request
    :return: a context for the template
    """
    current_route = request.matched_route.name
    return {
        'embed_js_url': request.route_path('embed'),
        'is_help': current_route == 'annotran_help',
        'is_onboarding': current_route == 'annotran_onboarding',
    }


def includeme(config):
    """
    Pyramid's includeme setup
    :param config: the configuration to which to add routes
    :return: None
    """
    config.add_route('annotran_help', '/docs/annotran_help')
    config.add_route('annotran_onboarding', '/annotran_welcome')

    config.scan(__name__)

from h import i18n
from h.api.views import json_view
from pyramid.view import (view_config, view_defaults)
import h.views

_ = i18n.TranslationStringFactory(__package__)


'''
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'annotran'}
'''

@view_config(renderer='templates/app.html.jinja2', route_name='app.html')
def __init__(self):
    return {'title': 'This is title', 'name': 'Home View'}


#@view_config(renderer='templates/login.html.jinja2', route_name='login.html')
#def home(self):
#    return {'title': 'This is title', 'name': 'Home View'}


@view_config(context=Exception, accept='text/html',
             renderer='h:templates/5xx.html.jinja2')
def error(context, request):
    """Display an error message."""
    h.views._handle_exc(request)
    return {'support_address': Shared.support_address}

@view_config(route_name='annotranhelp', renderer='templates/help.html.jinja2')
def help_page(request):
    return {'support_address': Shared.support_address}


@json_view(context=Exception)
def json_error(context, request):
    """"Return a JSON-formatted error message."""
    h.views._handle_exc(request)
    return {"reason": _(
        "Uh-oh, something went wrong! We're very sorry, our "
        "application wasn't able to load this page. The team has been "
        "notified and we'll fix it shortly. If the problem persists or you'd "
        "like more information please email {0} with the "
        "subject 'Internal Server Error'.").format(Shared.support_address)}

class Shared:
    support_address = ""


def includeme(config):
    config.add_route('annotranhelp', '/help')
    config.scan(__name__)
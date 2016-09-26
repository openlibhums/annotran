import h.views
from h import i18n
from h.api.views import json_view
from pyramid.view import (view_config)

_ = i18n.TranslationStringFactory(__package__)


@view_config(context=Exception, accept='text/html', renderer='h:templates/5xx.html.jinja2')
def error(context, request):
    """Display an error message."""
    h.views._handle_exc(request)
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


class Shared(object):
    def __init__(self):
        pass

    support_address = ""

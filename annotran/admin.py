from pyramid import view
from h import models


@view.view_config(route_name='admin_reports',
                  request_method='GET',
                  renderer='h:templates/admin/reports.html.jinja2',
                  permission='admin_reports')
def reports_index(_):
    return {}


def includeme(config):
    config.add_route('admin_reports', '/admin/reports')
    config.scan(__name__)
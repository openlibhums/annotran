from pyramid.view import (view_config, view_defaults)

'''
@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'annotran'}
'''

@view_defaults(renderer='templates/app.html.jinja2')
class Views:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='app.html')
    def home(self):
        return {'name': 'Home View'}

    @view_config(route_name='hello')
    def hello(self):
        return {'name': 'Hello View'}
from pyramid.view import (view_config, view_defaults)

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
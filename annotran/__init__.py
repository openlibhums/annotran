from pyramid.config import Configurator

def configure_jinja2_assets(config):
    assets_env = config.get_webassets_env()
    jinja2_env = config.get_jinja2_environment()
    jinja2_env.assets_environment = assets_env


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('home', '/')
    config.add_route('hello', '/howdy')
    config.scan('.views')
    return config.make_wsgi_app()

    '''
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()


    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_jinja2_extension('h.jinja_extensions.Filters')
    config.add_jinja2_extension('h.jinja_extensions.IncludeRawExtension')
    config.add_jinja2_extension('webassets.ext.jinja2.AssetsExtension')
    config.action(None, configure_jinja2_assets, args=(config,))

    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()

    '''


  #  config.add_route('hello', '/howdy')
   # config.scan('.views')

from pyramid.config import Configurator
from pyramid.threadlocal import get_current_registry

from pyramid_beaker import session_factory_from_settings
from pyramid_beaker import set_cache_regions_from_settings

from pyramid.threadlocal import get_current_registry

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    sessionFactory = session_factory_from_settings(settings)
    set_cache_regions_from_settings(settings)
    config = Configurator(settings=settings)
    config.set_session_factory(sessionFactory)
    get_current_registry().settings = settings
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('date', '/{channel}/{day}-{month}-{year}')
    config.include('pyramid_chameleon')
    config.scan()
    return config.make_wsgi_app()


import random

from pyramid.config import Configurator
from pyramid.events import NewResponse, NewRequest, subscriber
#from pyramid_beaker import set_cache_regions_from_settings
from pyramid_beaker import session_factory_from_settings

import logging; log = logging.getLogger(__name__)
DEBUG = log.debug; INFO = log.info; WARN = log.warning; ERROR = log.error

@subscriber(NewRequest)
def initialize_session(event):

    s = event.request.session
    if not 'team' in s:
        s['team'] = random.choice(['blue', 'red'])
    INFO("request team: %s" % s['team'])
    s.save()


@subscriber(NewResponse)
def add_cors_response_headers(event):

    INFO("new response: %s" % event)
    h = event.response.headers
    h.setdefault("Access-Control-Allow-Origin", "*")
    h.setdefault("Access-Control-Allow-Methods", "*")
    h.setdefault("Access-Control-Allow-Headers", "*")


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    session_factory = session_factory_from_settings(settings)
    #set_cache_regions_from_settings(settings)
    config = Configurator(settings=settings)
    config.set_session_factory(session_factory)
    config.include('pyramid_jinja2')
    config.include('.redis_store')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('controller', '/api/controller')
    config.add_route('game_state', '/api/game_state')
    config.add_route('game_config', '/api/game_config')
    config.scan()
    return config.make_wsgi_app()

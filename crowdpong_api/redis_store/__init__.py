import logging; log = logging.getLogger(__name__)
DEBUG = log.debug; INFO = log.info; WARN = log.warning; ERROR = log.error

from .store import RedisStore

def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('rht_survey.models')``.

    """
    settings = config.get_settings()

    store_url = settings.get('redis_store.url', 'redis://127.0.0.1:6379')
    store_prefix = settings.get('redis_store.url', 'redis_store')
    rstore = RedisStore(store_url, store_prefix)

    rstore["paddle_blue_v"] = 0.0;
    rstore["paddle_red_v"] = 0.0;
    rstore["paddle_delta_v"] = 0.1;
    rstore["paddle_max_v"] = 1.0;
    rstore["ball_v"] = 1.0;

    INFO("adding store")

    config.add_request_method(
        lambda x: rstore, 'redis_store', reify=True
    )

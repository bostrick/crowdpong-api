
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

    config.add_request_method(
        lambda x: rstore, 'redis_store', reify=True
    )

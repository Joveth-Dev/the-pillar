from django.core.cache import cache


def delete_cache_with_key_prefix(key_prefix):
    caches = cache.keys('*')
    print(f'CACHES: {caches}')
    cache.clear()
    print(f'CACHES: {caches}')
    if caches is not None:
        list_key = [key for key in caches if key_prefix in key]
    cache.delete_many(list_key)

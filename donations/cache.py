from django.core.cache import cache
from functools import wraps
from rest_framework.response import Response


def cache_response(key_prefix, timeout=60 * 15):
    """
    Декоратор для кэширования ответов ViewSet.
    """

    def decorator(view_method):
        @wraps(view_method)
        def _wrapped_view(self, request, *args, **kwargs):
            cache_key = f"{key_prefix}_{request.get_full_path()}"
            if request.method == "GET":
                cached_data = cache.get(cache_key)
                if cached_data is not None:
                    return Response(cached_data)
            response = view_method(self, request, *args, **kwargs)
            if request.method == "GET" and response.status_code == 200:
                cache.set(cache_key, response.data, timeout)
            return response

        return _wrapped_view

    return decorator


def invalidate_cache(key_prefix):
    """Инвалидирует все ключи с данным префиксом"""
    keys = cache.keys(f"{key_prefix}*")
    if keys:
        cache.delete_many(keys)

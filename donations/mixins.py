from .cache import invalidate_cache


class CacheResponseMixin:
    """
    Миксин для автоматического кэширования и инвалидации
    """
    CACHE_KEY_PREFIX = None
    CACHE_TIMEOUT = 60 * 5

    @classmethod
    def invalidate_class_cache(cls):
        if cls.CACHE_KEY_PREFIX:
            invalidate_cache(cls.CACHE_KEY_PREFIX)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.invalidate_class_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.invalidate_class_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self.invalidate_class_cache()

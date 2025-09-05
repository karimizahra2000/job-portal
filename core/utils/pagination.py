from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from urllib.parse import urlencode


class CachedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    cache_timeout = 60

    def _build_cache_key(self, request, view):
        page = request.query_params.get(self.page_query_param, 1)
        page_size = request.query_params.get(self.page_size_query_param, self.page_size)

        params = request.query_params.copy()
        params.pop(self.page_query_param, None)
        cache_suffix = urlencode(sorted(params.items()))

        return f"{view.__class__.__name__}:user={request.user.id}:page={page}:size={page_size}:{cache_suffix}"

    def paginate_queryset(self, queryset, request, view=None):
        cache_key = self._build_cache_key(request, view)
        cached_data = cache.get(cache_key)

        if cached_data:
            self._cached_page = True
            self._cached_response = cached_data
            self._cache_key = cache_key
            return cached_data["results"]

        self._cached_page = False
        self._cache_key = cache_key
        self.queryset = queryset
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)

        if not getattr(self, "_cached_page", False):
            cache.set(
                self._cache_key,
                {
                    "results": data,
                    "count": self.page.paginator.count,
                },
                timeout=self.cache_timeout,
            )

        return response

    @staticmethod
    def invalidate_cache_for_user(view_class, user_id):
        try:
            from django_redis import get_redis_connection
            redis_conn = get_redis_connection("default")
            pattern = f"{view_class.__name__}:user={user_id}:*"
            for key in redis_conn.scan_iter(pattern):
                redis_conn.delete(key)
        except ImportError:
            pass

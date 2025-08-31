import json
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CachedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

    def paginate_queryset(self, queryset, request, view=None):
        page = request.query_params.get(self.page_query_param, 1)
        page_size = request.query_params.get(self.page_size_query_param, self.page_size)

        cache_key = f"{view.__class__.__name__}:page={page}:size={page_size}:user={request.user.id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            self._cached_page = True
            self._cached_response = cached_data
            return cached_data["results"]

        self._cached_page = False
        self.queryset = queryset
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)

        if not getattr(self, "_cached_page", False):
            cache_key = f"{self.request.resolver_match.view_name}:page={self.page.number}:size={self.get_page_size(self.request)}:user={self.request.user.id}"
            cache.set(cache_key, {
                "results": data,
                "count": self.page.paginator.count,
            }, timeout=60)

        return response

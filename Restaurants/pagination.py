
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 4  # Default page size when page is requested
    page_query_param = 'page'

    def paginate_queryset(self, queryset, request, view=None):
        if self.page_query_param not in request.query_params:
            return None  # Return None to fetch all results when page is not provided
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        if not self.page.paginator.count:
            return Response(data)
        return super().get_paginated_response(data)


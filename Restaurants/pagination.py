
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

class CustomPagination(PageNumberPagination):
    page_size = 4  # Default page size when page is requested
    page_query_param = 'page'
    max_page_size = 3

    def paginate_queryset(self, queryset, request, view=None):
        if self.page_query_param not in request.query_params:
            return None  
        
        if not queryset.exists():
            raise NotFound('No data available')
        
        return super().paginate_queryset(queryset, request, view)


    def get_paginated_response(self, data):
        if not self.page.paginator.count:
            return Response(data)
        return super().get_paginated_response(data)


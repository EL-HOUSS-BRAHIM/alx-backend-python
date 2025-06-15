from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class for API responses.
    Returns 20 items per page with options to adjust via query parameters.
    """
    page_size = 20
    page_size_query_param = 'page_size'  # Allows ?page_size=10
    max_page_size = 100  # Limits maximum page size

    def get_paginated_response(self, data):
        """
        Customize the paginated response to include count, next, previous, and results.
        """
        return Response({
            'count': self.page.paginator.count,  
            'next': self.get_next_link(), 
            'previous': self.get_previous_link(),  
            'results': data  
        })
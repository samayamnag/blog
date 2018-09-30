from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
    )


class LargeResultsSetLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1000
    max_limit = 1500
    limit_query_param = 'limit'
    offset_query_param = 'offset'


class StandardResultsSetLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 1000
    limit_query_param = 'limit'
    offset_query_param = 'offset'


class LargeResultsSetPageNumberPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPageNumberPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

from rest_framework.pagination import PageNumberPagination, CursorPagination


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class MessageCursorPagination(CursorPagination):
    page_size = 20
    ordering = 'created_at'
    cursor_query_param = 'before'

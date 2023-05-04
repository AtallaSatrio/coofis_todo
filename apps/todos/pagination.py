from rest_framework.pagination import PageNumberPagination


class TodoPagination(PageNumberPagination):
    def __init__(self, limit):
        self.page_size = limit

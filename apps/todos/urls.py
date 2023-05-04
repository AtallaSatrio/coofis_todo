from django.urls import include, path
from apps.todos.views import todo_views

app_name = "todos"
urlpatterns = [
    path("test/", todo_views.TodoDestroyAPIView.as_view(), name="test"),
    path("destroy/", todo_views.TodoDestroyAPIView.as_view(), name="hello"),
    path(
        "submit/", todo_views.TodoListCreateAPIView.as_view(), name="action-submit-todo"
    ),
    path("", todo_views.TodoListCreateAPIView.as_view(), name="list-todo"),
    path(
        "<str:id>/",
        todo_views.TodoRetrieveUpdateAPIView.as_view(),
        name="retrieve-todo",
    ),
    path(
        "<str:id>/update/",
        todo_views.TodoRetrieveUpdateAPIView.as_view(),
        name="update-todo",
    ),
]

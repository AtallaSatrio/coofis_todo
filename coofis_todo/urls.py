from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("account/", include("apps.accounts.urls")),
                path("todo/", include("apps.todos.urls")),
            ]
        ),
    ),
]

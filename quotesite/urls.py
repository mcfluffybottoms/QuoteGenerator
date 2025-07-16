from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("", RedirectView.as_view(url="/polls/", permanent=False)),
    path("admin/", admin.site.urls),
]

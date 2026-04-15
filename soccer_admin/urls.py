from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("teams/", include("teams.urls")),
    path("leagues/", include("leagues.urls")),
    path("matches/", include("matches.urls")),
]

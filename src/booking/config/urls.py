from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .. import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("social/", include("social_django.urls", namespace="social")),
    path("", views.Index.as_view(template_name="index.html"), name="index"),
    path("home/", views.Home.as_view(template_name="home.html"), name="home"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
admin.autodiscover()

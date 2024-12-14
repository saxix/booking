from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .. import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("social/", include("social_django.urls", namespace="social")),
    path("", views.Index.as_view(), name="index"),
    path("home/", views.Home.as_view(template_name="home.html"), name="home"),
    path("properties/", views.AccommodationView.as_view(), name="property-list"),
    path("bookings/", views.BookingView.as_view(), name="booking-list"),
    path("bookings/<int:property>/add/", views.CreateBookView.as_view(), name="booking-add"),
    path("bookings/<int:book>/cancel/", views.CancelBookView.as_view(), name="booking-cancel"),
    path("login/", views.Index.as_view(template_name="index.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
admin.autodiscover()

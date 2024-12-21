from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .. import views

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("social/", include("social_django.urls", namespace="social")),
    path("", views.Index.as_view(), name="index"),
    # path("", views.Index.as_view(), name="login"),
    path("fleet/", views.FleetView.as_view(), name="car-list"),
    path("bookings/", views.BookingView.as_view(), name="booking-list"),
    path("bookings/<int:car>/add/", views.CreateBookView.as_view(), name="booking-add"),
    path(
        "bookings/<int:book>/cancel/",
        views.CancelBookView.as_view(),
        name="booking-cancel",
    ),
    # path("manager/cars/", views.FleetView.as_view(manager=True), name="car-list"),
    # path(
    #     "manager/bookings/",
    #     views.BookingView.as_view(manager=True),
    #     name="booking-list",
    # ),
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("healthcheck/", views.healthcheck, name="healthcheck"),
)

if "django_browser_reload" in settings.INSTALLED_APPS:  # pragma: no cover
    urlpatterns += [path(r"__reload__/", include("django_browser_reload.urls"))]

admin.autodiscover()

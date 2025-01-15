from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from .. import views

handler400 = views.error_400
handler403 = views.error_403
handler404 = views.error_404
handler500 = views.error_500

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("social/", include("social_django.urls", namespace="social")),
    path("", views.Index.as_view(), name="index"),
    path("fleet/", views.FleetView.as_view(), name="car-list"),
    path("bookings/", views.BookingView.as_view(), name="booking-list"),
    path("bookings/<int:car>/add/", views.CreateBookView.as_view(), name="booking-add"),
    path(
        "bookings/<int:book>/cancel/",
        views.CancelBookView.as_view(),
        name="booking-cancel",
    ),
    path("login/", views.LoginView.as_view(), name="login"),
    path("otp/<str:key>/", views.OTPLoginView.as_view(), name="otp-login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("registered/", views.RegisterCompleteView.as_view(), name="register-complete"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("healthcheck/", views.healthcheck, name="healthcheck"),
    # utility urls
    path("errors/400/", handler400, name="errors-400"),
    path("errors/403/", handler403, name="errors-403"),
    path("errors/404/", handler404, name="errors-404"),
    path("errors/500/", handler500, name="errors-500"),
)

if "django_browser_reload" in settings.INSTALLED_APPS:  # pragma: no cover
    urlpatterns += [path(r"__reload__/", include("django_browser_reload.urls"))]

admin.autodiscover()

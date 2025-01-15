from typing import Any

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as LoginView_
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.crypto import get_random_string, md5
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.http import condition
from django.views.generic import CreateView, DeleteView, ListView, RedirectView, TemplateView

from booking.config import env
from booking.exceptions import CollisionError, RecordChanged
from booking.forms import CreateBookingForm, LoginForm, RegisterForm
from booking.models import Booking, Car, User


def get_fleet_version_key(request, *args, **kwargs):
    etag_key = f"etag:{request.user.username}:{Car.get_cache_version()}"
    return md5(etag_key.encode("utf-8")).hexdigest()


def get_booking_version_key(request, *args, **kwargs):
    etag_key = f"etag:{request.user.username}:{Car.get_cache_version()}:{Booking.get_cache_version()}"
    return md5(etag_key.encode("utf-8")).hexdigest()


class FleetConditionMixin:
    @method_decorator(condition(etag_func=get_fleet_version_key, last_modified_func=None))
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        response["Cache-Control"] = "public"
        return response


class CommonContextMixin:
    """Common context mixin for all views. Used to add common data to UI."""

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["active_view"] = self.__class__.__name__
        kwargs["sso_enabled"] = bool(settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)
        return super().get_context_data(**kwargs)


class RegisterCompleteView(CommonContextMixin, TemplateView):
    template_name = "registered.html"


class RegisterView(CommonContextMixin, CreateView):
    """New user registration view."""

    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if "form" in kwargs and not kwargs["form"].is_valid():
            kwargs["invalid_post"] = True
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        ret = super().form_valid(form)
        otp = get_random_string(128)
        cache.set(f"otp:{otp}", self.object.pk, timeout=86400)
        url = self.request.build_absolute_uri(reverse("otp-login", args=[otp]))
        subject = "Grazie per la registrazione a Booking"
        text_content = f"Per accedere fai click su questo link <a href='{url}'>{url}</a>"

        msg = EmailMessage(subject, text_content, env("GMAIL_USER"), [self.object.email])
        msg.content_subtype = "html"
        msg.send()
        return ret


class OTPLoginView(CommonContextMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        pk = cache.get(f"otp:{self.kwargs['key']}")
        if not pk:
            raise Http404
        else:
            user = User.objects.get(pk=pk)
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return HttpResponseRedirect(reverse("index"))


class LoginView(CommonContextMixin, LoginView_):
    """Login view."""

    template_name = "login.html"
    form_class = LoginForm


class Index(CommonContextMixin, FleetConditionMixin, TemplateView):
    """Home page view."""

    template_name = "index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if not (home_page_models := Car.get_from_cache("home_page_models")):
            home_page_models = list(Car.objects.values("model", "image", "pk", "price")[:4])
            Car.store_to_cache(home_page_models, "home_page_models")
        kwargs["models"] = home_page_models
        return super().get_context_data(**kwargs)


class FleetView(CommonContextMixin, FleetConditionMixin, ListView):
    """Full fleet page view."""

    template_name = "fleet.html"

    def get_queryset(self) -> QuerySet[Car]:
        key = "fleet"
        if not (fleet := Car.get_from_cache(key)):
            fleet = list(Car.objects.values())
            Car.store_to_cache(fleet, key)

        return fleet


class CancelBookView(CommonContextMixin, LoginRequiredMixin, DeleteView):
    """User booking cancellation view."""

    template_name = "book_delete.html"
    pk_url_kwarg = "book"
    success_url = reverse_lazy("booking-list")

    def get_queryset(self) -> QuerySet[Booking]:
        return Booking.objects.filter(customer=self.request.user)

    def get_object(self, queryset: QuerySet[Booking] | None = None) -> Booking:
        return self.get_queryset().get(pk=self.kwargs.get(self.pk_url_kwarg))


class CreateBookView(CommonContextMixin, LoginRequiredMixin, CreateView):
    """Create new booking view."""

    template_name = "book_add.html"
    queryset = Booking.objects.all()
    form_class = CreateBookingForm
    success_url = reverse_lazy("booking-list")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["car"] = self.selected_car
        return super().get_context_data(**kwargs)

    @cached_property
    def selected_car(self) -> Car:
        return Car.objects.get(pk=self.kwargs["car"])

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["car"] = self.selected_car
        return kwargs

    def get_initial(self) -> dict[str, Any]:
        return {
            "start_date": timezone.now(),
            "end_date": timezone.now(),
            "car_version": self.selected_car.version,
        }

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form: ModelForm) -> HttpResponseRedirect | HttpResponse:
        form.instance.car = self.selected_car
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseRedirect | HttpResponse:
        self.object = None
        form = self.get_form()
        if form.is_valid():
            try:
                ret = self.form_valid(form)
                return ret
            except (RecordChanged, CollisionError):
                return self.form_invalid(form)
            finally:
                Booking.invalidate_cache()
        else:
            return self.form_invalid(form)


class BookingView(CommonContextMixin, LoginRequiredMixin, ListView):
    """User personal booking list view."""

    template_name = "bookings.html"
    manager = False

    def get_queryset(self) -> QuerySet[Car]:
        key = f"my-booking:{self.request.user.username}"
        if not (fleet := Booking.get_from_cache(key)):
            fleet = Booking.objects.filter(customer=self.request.user)
            Booking.store_to_cache(fleet, key)

        return fleet

    @method_decorator(condition(etag_func=get_booking_version_key, last_modified_func=None))
    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        response["Cache-Control"] = "private, max-age=0"
        return response


def healthcheck(request: "HttpRequest") -> HttpResponse:
    """Healthcheck endpoint. Used to check the health of the server.

    :param request: HttpRequest
    :rtype: HttpResponse
    """
    return HttpResponse("Ok")


def error_400(request: HttpRequest, exception: Exception = None) -> HttpResponse:
    return render(request, "errors/400.html", {"error_code": 400, "message": "Bad Request"}, status=400)


def error_403(request: HttpRequest, exception: Exception = None) -> HttpResponse:
    return render(request, "errors/403.html", {"error_code": 403, "message": "Forbidden"}, status=403)


def error_404(request: HttpRequest, exception: Exception = None) -> HttpResponse:
    return render(request, "errors/404.html", {"error_code": 404, "message": "Page not found"}, status=404)


def error_500(request: HttpRequest, exception: Exception = None) -> HttpResponse:
    return render(request, "errors/500.html", {"error_code": 500, "message": "Server Error"}, status=500)

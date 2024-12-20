from typing import Any, Optional

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as LoginView_
from django.core.cache import cache
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.functional import cached_property
from django.views.generic import CreateView, DeleteView, ListView, TemplateView

from booking.exceptions import RecordChanged
from booking.forms import CreateBookingForm, LoginForm, RegisterForm
from booking.models import Booking, Car


class CommonContextMixin:

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["active_view"] = self.__class__.__name__
        kwargs["sso_enabled"] = bool(settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)

        return super().get_context_data(**kwargs)


class RegisterView(CommonContextMixin, CreateView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("index")


class LoginView(CommonContextMixin, LoginView_):
    template_name = "login.html"
    form_class = LoginForm


class Index(CommonContextMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if not (home_page_models := cache.get("home_page_models")):
            home_page_models = list(Car.objects.values("model", "image", "pk", "price")[:4])
            cache.set("home_page_models", home_page_models)
        kwargs["models"] = home_page_models
        return super().get_context_data(**kwargs)


class FleetView(CommonContextMixin, ListView):
    manager = False
    template_name = "fleet.html"

    def get_queryset(self) -> QuerySet[Car]:
        base = "fleet"
        v = cache.get(f"version:{base}") or 1
        key = f"{base}:{v}"
        if not (fleet := cache.get(key)):
            fleet = list(Car.objects.values())
            cache.set(key, fleet)

        return fleet


class CancelBookView(CommonContextMixin, LoginRequiredMixin, DeleteView):
    template_name = "book_delete.html"
    pk_url_kwarg = "book"
    success_url = reverse_lazy("booking-list")

    def get_queryset(self) -> QuerySet[Booking]:
        return Booking.objects.filter(customer=self.request.user)

    def get_object(self, queryset: Optional[QuerySet[Booking]] = None) -> Booking:
        return self.get_queryset().get(pk=self.kwargs.get(self.pk_url_kwarg))


class CreateBookView(CommonContextMixin, LoginRequiredMixin, CreateView):
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
            "car_version": self.selected_car.version,
            "end_date": timezone.now(),
        }

    def form_valid(self, form: ModelForm) -> HttpResponseRedirect | HttpResponse:
        form.instance.car = self.selected_car
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseRedirect | HttpResponse:
        self.object = None
        form = self.get_form()
        if form.is_valid():
            try:
                return self.form_valid(form)
            except RecordChanged:
                return self.form_invalid(form)

        else:
            return self.form_invalid(form)


class BookingView(CommonContextMixin, LoginRequiredMixin, ListView):
    template_name = "bookings.html"
    manager = False

    def get_queryset(self) -> QuerySet[Booking]:
        return Booking.objects.filter(customer=self.request.user)


def healthcheck(request: "HttpRequest") -> HttpResponse:
    return HttpResponse("Ok")

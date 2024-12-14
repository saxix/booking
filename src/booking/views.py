from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, TemplateView

from booking.forms import CreateBookingForm
from booking.models import Accommodation, Booking


class CommonContextMixin:

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["active_view"] = self.__class__.__name__
        return super().get_context_data(**kwargs)


class Index(CommonContextMixin, TemplateView):
    template_name = "index.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseRedirect | HttpResponse:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        return super().get(request, *args, **kwargs)


class Home(CommonContextMixin, LoginRequiredMixin, TemplateView):
    pass


class AccommodationView(CommonContextMixin, LoginRequiredMixin, ListView):
    template_name = "places.html"
    queryset = Accommodation.objects.all()


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

    def get_property(self) -> Accommodation:
        return Accommodation.objects.get(pk=self.kwargs["property"])

    def get_initial(self) -> dict[str, Any]:
        return {
            "start_date": timezone.now(),
            "property_version": self.get_property().version,
            "end_date": timezone.now(),
        }

    def form_valid(self, form: ModelForm) -> HttpResponseRedirect | HttpResponse:
        form.instance.property = self.get_property()
        form.instance.customer = self.request.user
        return super().form_valid(form)


class BookingView(CommonContextMixin, LoginRequiredMixin, ListView):
    template_name = "bookings.html"

    def get_queryset(self) -> QuerySet[Booking]:
        return Booking.objects.filter(customer=self.request.user)

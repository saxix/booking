from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.functional import cached_property
from django.views.generic import CreateView, DeleteView, ListView, TemplateView

from booking.exceptions import PeriodNotAvailable, RecordChanged
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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs["property"] = self.selected_place
        return super().get_context_data(**kwargs)

    @cached_property
    def selected_place(self) -> Accommodation:
        return Accommodation.objects.get(pk=self.kwargs["property"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["place"] = self.selected_place
        return kwargs

    def get_initial(self) -> dict[str, Any]:
        return {
            "start_date": timezone.now(),
            "place_version": self.selected_place.version,
            "end_date": timezone.now(),
        }

    def form_valid(self, form: ModelForm) -> HttpResponseRedirect | HttpResponse:
        form.instance.property = self.selected_place
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
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

    def get_queryset(self) -> QuerySet[Booking]:
        return Booking.objects.filter(customer=self.request.user)

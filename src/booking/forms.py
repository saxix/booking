from django import forms
from django.db.transaction import atomic

from booking.exceptions import PeriodNotAvailable, RecordChanged
from booking.models import Booking, Car
from typing import TYPE_CHECKING

from booking.utils.booking import is_available


class CreateBookingForm(forms.ModelForm):
    car_version = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Booking
        fields = ("start_date", "end_date")

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop("car")
        assert self.car, "place must be specified"
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if not is_available(self.car, self.cleaned_data.get("start_date", None), self.cleaned_data.get("end_date", None)):
            raise forms.ValidationError("Selected period is not available")

    def save(self, commit: bool = True) -> Booking:
        days = (self.instance.end_date - self.instance.start_date).days

        with atomic():
            lock: Car = Car.objects.select_for_update().get(pk=self.car.pk)
            if lock.version != self.cleaned_data["car_version"]:
                self.add_error(None, RecordChanged.message)
                raise RecordChanged()
            if is_available(self.car, self.instance.start_date, self.instance.end_date):
                self.instance.total_price = self.instance.property.price * days
                super().save(commit)
                self.instance.property.save(update_fields=[ "version"])
            else:
                raise forms.ValidationError(PeriodNotAvailable)
        return self.instance

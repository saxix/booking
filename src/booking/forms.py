from django import forms
from django.db.transaction import atomic

from booking.exceptions import PeriodNotAvailable, RecordChanged
from booking.models import Booking, Accommodation
from typing import TYPE_CHECKING

from booking.utils.booking import is_available


class CreateBookingForm(forms.ModelForm):
    place_version = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Booking
        fields = ("start_date", "end_date")

    def __init__(self, *args, **kwargs):
        self.place = kwargs.pop("place")
        assert self.place, "place must be specified"
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if not is_available(self.place, self.cleaned_data["start_date"], self.cleaned_data["end_date"]):
            raise forms.ValidationError("Selected period is not available")

    def save(self, commit: bool = True) -> Booking:
        days = (self.instance.end_date - self.instance.start_date).days

        with atomic():
            lock: Accommodation = Accommodation.objects.select_for_update().get(pk=self.place.pk)
            if lock.version != self.cleaned_data["place_version"]:
                self.add_error(None, RecordChanged.message)
                raise RecordChanged()
            if is_available(self.place, self.instance.start_date, self.instance.end_date):
                self.instance.total_price = self.instance.property.price * days
                super().save(commit)
                self.instance.property.is_available = False
                self.instance.property.save(update_fields=["is_available", "version"])
            else:
                raise forms.ValidationError(PeriodNotAvailable)
        return self.instance

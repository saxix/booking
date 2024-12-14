from django import forms
from django.db.transaction import atomic

from booking.models import Booking


class CreateBookingForm(forms.ModelForm):
    property_version = forms.IntegerField()

    class Meta:
        model = Booking
        fields = ("start_date", "end_date")

    def save(self, commit: bool = True) -> Booking:
        days = (self.instance.end_date - self.instance.start_date).days
        with atomic():
            self.instance.total_price = self.instance.property.price * days
            super().save(commit)
            self.instance.property.is_available = False
            self.instance.property.save(update_fields=["is_available", "version"])
        return self.instance

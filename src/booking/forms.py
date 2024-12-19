from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.transaction import atomic

from booking.exceptions import PeriodNotAvailable, RecordChanged
from booking.models import Booking, Car, User
from typing import TYPE_CHECKING

from booking.utils.booking import is_available


class DateInput(forms.DateInput):
    input_type = "date"


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password"]


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"autofocus": True}))

    class Meta:
        model = User
        fields = ["email", "password"]


class CreateBookingForm(forms.ModelForm):
    car_version = forms.IntegerField(widget=forms.HiddenInput())
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Booking
        fields = ("start_date", "end_date")

    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop("car")
        assert self.car, "place must be specified"
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        if not is_available(self.car, self.cleaned_data.get("start_date", None),
                            self.cleaned_data.get("end_date", None)):
            raise forms.ValidationError("Selected period is not available")

    def save(self, commit: bool = True) -> Booking:
        days = (self.instance.end_date - self.instance.start_date).days

        with atomic():
            lock: Car = Car.objects.select_for_update().get(pk=self.car.pk)
            if lock.version != self.cleaned_data["car_version"]:
                self.add_error(None, RecordChanged.message)
                raise RecordChanged()
            if is_available(self.car, self.instance.start_date, self.instance.end_date):
                self.instance.total_price = self.instance.car.price * days
                super().save(commit)
                self.instance.car.save(update_fields=["version"])
            else:
                raise forms.ValidationError(PeriodNotAvailable)
        return self.instance

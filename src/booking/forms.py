from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.db import OperationalError
from django.db.transaction import atomic
from django.utils.translation import gettext as _

from booking.exceptions import CollisionError, RecordChanged
from booking.models import Booking, Car, User
from booking.utils.booking import is_available


class DateInput(forms.DateInput):
    """Force HTML date input type for DateInput. Overrides default Django behavior."""

    input_type = "date"


class RegisterForm(forms.ModelForm):
    """Form to register a user."""

    username = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password")

    def save(self, commit: bool = True) -> Car:
        self.instance.email = self.instance.username
        self.instance.password = make_password(self.cleaned_data["password"])
        return super().save(commit)


class LoginForm(AuthenticationForm):
    """Local login form."""

    username = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"autofocus": True}))

    class Meta:
        model = User
        fields = ("username", "password")


class CreateBookingForm(forms.ModelForm):
    """Form to create a booking."""

    car_version = forms.IntegerField(widget=forms.HiddenInput())
    start_date = forms.DateField(widget=DateInput())
    end_date = forms.DateField(widget=DateInput())

    class Meta:
        model = Booking
        fields = ("start_date", "end_date")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.car = kwargs.pop("car")
        super().__init__(*args, **kwargs)

    def clean(self) -> None:
        super().clean()
        if not is_available(
            self.car,
            self.cleaned_data.get("start_date", None),
            self.cleaned_data.get("end_date", None),
        ):
            raise forms.ValidationError("Selected period is not available")

    def save(self, commit: bool = True) -> Booking:
        days = (self.instance.end_date - self.instance.start_date).days
        with atomic():
            """wraps into transaction to lock the record and prevent conflicts."""
            try:
                lock: Car = Car.objects.select_for_update(nowait=True).get(pk=self.car.pk)
                if lock.version != self.cleaned_data["car_version"]:
                    self.add_error(None, RecordChanged.message)
                    raise RecordChanged()
                self.instance.total_price = self.instance.car.price * days
                self.instance = super().save(commit)
            except OperationalError:
                raise CollisionError(_("Period is not available"))
        return self.instance

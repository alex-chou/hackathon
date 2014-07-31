from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User

from hackathon.core.models import Recreation, Reservation

class RecreationForm(forms.ModelForm):
    class Meta:
        model = Recreation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ("active", "created_at")

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields["start_time"].widget = widgets.AdminTimeWidget()
        self.fields["end_time"].widget = widgets.AdminTimeWidget()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "password", "username")

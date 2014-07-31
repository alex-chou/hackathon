from django import forms
from django.contrib.auth.models import User

from hackathon.core.models import Recreation, Reservation

class RecreationForm(forms.ModelForm):
    class Meta:
        model = Recreation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ("active", "created_at")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "password", "username")

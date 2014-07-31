from django import forms
from django.contrib.auth.models import User

from hackathon.core.models import Recreation, Reservation

def RecreationForm(forms.ModelForm):
    class Meta:
        model = Recreation

def ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ("active", "created_at")

def UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "password", "username")

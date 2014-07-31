from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from hackathon.core.forms import RecreationForm, ReservationForm, UserForm
from hackathon.core.models import Recreation, Reservation, User

@csrf_exempt
def create_recreation(request, template_name="create-recreation.html"):
    if request.method == "POST":
        form = RecreationForm(data=request.POST)
        try:
            if form.errors:
                raise forms.ValidationError(form.errors)

            Recreation.objects.create(
                name = form.cleaned_data["name"],
                max_duration = form.cleaned_data["max_duration"],
                reservation_cooldown = form.cleaned_data["reservation_cooldown"]
            )
            return HttpResponse("success")
        except forms.ValidationError:
            return render_to_response(template_name, {"recreation_form": form}, context_instance=RequestContext(request))
    else:
        form = RecreationForm()

    return render_to_response(template_name, {"recreation_form": form})

@csrf_exempt
def create_reservation(request, template_name="create-reservation.html"):
    if request.method == "POST":
        form = ReservationForm(data=request.POST)
        try:
            if form.errors:
                raise forms.ValidationError(form.errors)

            Reservation.objects.create(
                notes = form.cleaned_data["notes"],
                start_time = form.cleaned_data["start_time"],
                end_time = form.cleaned_data["end_time"],
                user = request.user,
                recreation = form.cleaned_data["recreation"]
            )
            return HttpResponse("success")
        except forms.ValidationError:
            return render_to_response(template_name, {"reservation_form": form}, context_instance=RequestContext(request))
    else:
        form = ReservationForm()

    return render_to_response(template_name, {"reservation_form": form})

@csrf_exempt
def create_user(request, template_name="create-user.html"):
    if request.method == "POST":
        form = UserForm(data=request.POST)
        try:
            if form.errors:
                raise forms.ValidationError(form.errors)

            User.objects.create(
                email = form.cleaned_data["email"],
                username = form.cleaned_data["username"],
                password = form.cleaned_data["password"]
            )
            return HttpResponse("success")
        except forms.ValidationError:
            return render_to_response(template_name, {"user_form": form}, context_instance=RequestContext(request))
    else:
        form = UserForm()

    return render_to_response(template_name, {"user_form": form})

def index(request, template_name="index.html"):
    return render_to_response(template_name)

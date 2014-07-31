from datetime import datetime, timedelta

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
    success = ""
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
            success = "recreation created!"
            form = RecreationForm()
        except forms.ValidationError:
            return render_to_response(template_name, {"recreation_form": form}, context_instance=RequestContext(request))
    else:
        form = RecreationForm()

    return render_to_response(template_name, {"recreation_form": form, "success": success})

@csrf_exempt
def create_reservation(request, template_name="create-reservation.html"):
    success = ""
    if request.method == "POST":
        form = ReservationForm(data=request.POST)
        try:
            if form.errors or\
                    not User.objects.filter(email=form.cleaned_data["email"]) or\
                    not User.objects.get(email=form.cleaned_data["email"]).check_password(form.cleaned_data["password"]):
                raise forms.ValidationError(form.errors)
            start_date = datetime.today() if form.cleaned_data["date_choices"] == u"today" else datetime.today() + timedelta(days=1)
            start_datetime = datetime.combine(start_date, datetime.strptime(form.cleaned_data["time_choices"], "%H:%M").time())
            end_datetime = start_datetime + timedelta(minutes=form.cleaned_data["duration"])

            Reservation.objects.create(
                notes = form.cleaned_data["notes"],
                start_time = start_datetime,
                end_time = end_datetime,
                recreation = form.cleaned_data["recreation"],
                user = User.objects.get(email=form.cleaned_data["email"])
            )
            success = "%s reserved!" % form.cleaned_data["recreation"].name
            form = ReservationForm()
        except forms.ValidationError:
            return render_to_response(template_name, {"reservation_form": form}, context_instance=RequestContext(request))
    else:
        form = ReservationForm()

    return render_to_response(template_name, {"reservation_form": form, "success": success})

@csrf_exempt
def create_user(request, template_name="create-user.html"):
    success = ""
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
            success = "user created!"
            form = UserForm()
        except forms.ValidationError:
            return render_to_response(template_name, {"user_form": form}, context_instance=RequestContext(request))
    else:
        form = UserForm()

    return render_to_response(template_name, {"user_form": form, "success": success})

def index(request, template_name="index.html"):
    return render_to_response(template_name)

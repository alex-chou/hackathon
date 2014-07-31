from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from core.models import Recreation, Reservation


class RecreationResource(ModelResource):
    class Meta:
        queryset = Recreation.objects.all()
        resource_name = "recreations"


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = "users"


class ReservationResource(ModelResource):
    class Meta:
        queryset = Reservation.objects.all()
        resource_name = "reservations"

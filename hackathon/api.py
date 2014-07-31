from django.contrib.auth.models import User
from django.http import HttpResponse
from tastypie import http
from tastypie.resources import ModelResource
from tastypie.exceptions import ImmediateHttpResponse
from core.models import Recreation, Reservation


class CORSResource(ModelResource):
    """
        Adds CORS headers to resources that subclass this.
    """
    def create_response(self, *args, **kwargs):
        response = super(CORSResource, self).create_response(*args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def method_check(self, request, allowed=None):
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        allows = ','.join([_.upper() for _ in allowed])

        if request_method == 'options':
            response = HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method


class RecreationResource(CORSResource):
    class Meta:
        queryset = Recreation.objects.all()
        resource_name = "recreations"


class UserResource(CORSResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = "users"


class ReservationResource(CORSResource):
    class Meta:
        queryset = Reservation.objects.all()
        resource_name = "reservations"

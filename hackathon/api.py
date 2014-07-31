import datetime

from django.db.models import Q
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User

from tastypie import fields, http
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
            response = http.HttpResponse(allows)
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if not request_method in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method

    def deserialize(self, request, data, format=None):

        if not format:
            format = request.META.get("CONTENT_TYPE", "application/json")

        if format == "application/x-www-form-urlencoded":
            return request.POST

        if format.startswith("multipart"):
            data = request.POST.copy()
            data.update(request.FILES)

            return data

        return super(CORSResource, self).deserialize(request, data, format)


class RecreationResource(CORSResource):
    class Meta:
        queryset = Recreation.objects.all()
        resource_name = "recreations"
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]

    def obj_create(self, bundle, **kwargs):
        bundle.obj = Recreation.objects.create(
            name=bundle.data.get("name"),
            max_duration=bundle.data.get("max_duration", 0),
            reservation_cooldown=bundle.data.get("reservation_cooldown", 0)
        )

        return bundle


class UserResource(CORSResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = "users"
        detail_allowed_methods = ["get"]
        list_allowed_methods = ["get"]
        excludes = ["password", "is_staff", "is_active", "is_superuser", "first_name", "last_name"]


class ReservationResource(CORSResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    recreation = fields.ForeignKey(RecreationResource, 'recreation', full=True)

    class Meta:
        queryset = Reservation.objects.all()
        resource_name = "reservations"
        detail_allowed_methods = ["get", "post"]
        list_allowed_methods = ["get", "post"]

    def obj_create(self, bundle, **kwargs):
        now = datetime.datetime.now()

        email = bundle.data.get("email", "").lower()
        username = email.split("@")[0]
        password = bundle.data.get("password")
        recreation_id = bundle.data.get("recreation_id")
        notes = unicode(bundle.data.get("notes", ""))
        start_time = bundle.data.get("start_time", now)
        end_time = bundle.data.get("end_time", now + datetime.timedelta(minutes=30))

        if not all([email, username, password]):
            response = http.HttpResponse("Error: some shiz broke")
            response.status_code = 400
            raise ImmediateHttpResponse(response=response)

        recreation = Recreation.objects.filter(id=recreation_id)
        recreation = recreation[0] if recreation else None
        if not recreation:
            recreation = Recreation.objects.get(name="Ping Pong")

        user, created = User.objects.get_or_create(
            email=email,
            defaults=dict(
                password=make_password(password),
                username=email.split("@")[0]
            )
        )

        if not created and not check_password(password, user.password):
            response = http.HttpResponse("Error: incorrect password")
            response.status_code = 400
            raise ImmediateHttpResponse(response=response)

        # check time conflicts
        query = Q(start_time__lt=start_time, end_time__gt=start_time) | Q(start_time__lt=end_time, end_time__gt=end_time)

        reservations = Reservation.objects.filter(recreation=recreation, end_time__gt=now)\
            .filter(query)
        if reservations:
            response = http.HttpResponse("Error: someone already has a reservation")
            response.status_code = 400
            raise ImmediateHttpResponse(response=response)

        bundle.obj = Reservation.objects.create(
            active=True,
            created_at=datetime.datetime.now(),
            end_time=end_time,
            notes=notes,
            recreation=recreation,
            start_time=start_time,
            user=user,
        )

        return bundle

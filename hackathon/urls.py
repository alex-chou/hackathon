from django.conf.urls import patterns, include, url
from api import RecreationResource, ReservationResource, UserResource


from django.contrib import admin
admin.autodiscover()

# adding something just to create trivial commit
print "hello"
# initialize API ModelResources
recreation_resource = RecreationResource()
reservation_resource = ReservationResource()
user_resource = UserResource()

urlpatterns = patterns('',
    url(r'^$', 'hackathon.core.views.index', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^recreation/', 'hackathon.core.views.create_recreation',
        name='recreation'),
    url(r'^reservation/', 'hackathon.core.views.create_reservation',
        name='reservation'),
    url(r'^user/', 'hackathon.core.views.create_user', name='user'),
    # REST-ful API urls:
    url(r'^api/', include(recreation_resource.urls)),
    url(r'^api/', include(reservation_resource.urls)),
    url(r'^api/', include(user_resource.urls)),
)

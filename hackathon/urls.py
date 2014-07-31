from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^recreation/', 'hackathon.core.views.create_recreation',
            name='recreation'),
        url(r'^reservation/', 'hackathon.core.views.create_reservation',
            name='reservation'),
        url(r'^user/', 'hackathon.core.views.create_user', name='user'),
)

from django.contrib.auth.models import User
from django.db.models import (BooleanField, CharField, DateTimeField, ForeignKey, IntegerField,
    Model, OneToOneField)

class Recreation(Model):
    name = CharField(max_length=70, null=True, blank=True, db_index=True)
    max_duration = IntegerField()
    reservation_cooldown = IntegerField()

    def __unicode__(self):
        return u"%s" % name

class Reservation(Model):
    active = BooleanField(default=True)
    notes = CharField(max_length=100, null=True, blank=True, db_index=True)
    created_at = DateTimeField(db_index=True, auto_now_add=True)
    start_time = DateTimeField(null=True, blank=True, db_index=True)
    end_time = DateTimeField(null=True, blank=True, db_index=True)
    user = ForeignKey(User)
    recreation = OneToOneField(Recreation, related_name="recreation")

    def __unicode__(self):
        return u"%s reserved" % self.recreation.name

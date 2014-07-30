from django.db.models import (BooleanField, CharField, DateTimeField, ForeignKey, IntegerField,
    Model, OneToOneField)

class User(Model):
    is_superuser = BooleanField(default=False)

class UserProfile(Model):
    email = CharField(max_length=75, unique=True, null=True, blank=True)
    password = CharField(max_length=128, null=True, blank=True)
    name = CharField(max_length=70, null=True, blank=True, db_index=True)
    user = OneToOneField(User, related_name="user_profile")

class Recreation(Model):
    name = CharField(max_length=70, null=True, blank=True, db_index=True)
    max_duration = IntegerField()
    reservation_cooldown = IntegerField()

class Reservation(Model):
    active = BooleanField(default=True)
    created_at = DateTimeField(db_index=True, auto_now_add=True)
    start_time = DateTimeField(null=True, blank=True, db_index=True)
    end_time = DateTimeField(null=True, blank=True, db_index=True)
    user_profile = ForeignKey(UserProfile)
    recreation = OneToOneField(Recreation, related_name="recreation")

from django.contrib import admin
from models import Recreation, Reservation

class RecreationAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "max_duration", "reservation_cooldown"]
    search_fields = ["name"]

class ReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "notes", "created_at"]
    raw_id_fields = ["user"]


# register the admins
admin.site.register(Recreation, RecreationAdmin)
admin.site.register(Reservation, ReservationAdmin)


from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    fields = [
        "client_id",
        "support_contact_id",
        "event_status",
        "attendees",
        "event_date",
        "notes",
    ]
    list_display = (
        "client_id",
        "support_contact_id",
        "event_status",
        "attendees",
        "event_date",
        "notes",
        "date_created",
        "date_updated",
    )


admin.site.register(Event, EventAdmin)

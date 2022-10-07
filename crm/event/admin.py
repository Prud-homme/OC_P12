from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    fields = [
        "client",
        "support_contact",
        "event_status",
        "attendees",
        "event_date",
        "notes",
    ]
    list_display = (
        "client",
        "support_contact",
        "event_status",
        "attendees",
        "event_date",
        "notes",
        "date_created",
        "date_updated",
    )


admin.site.register(Event, EventAdmin)

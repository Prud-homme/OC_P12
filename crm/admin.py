from django.contrib import admin

from .models import Client, Contract, Event


class ClientAdmin(admin.ModelAdmin):
    fields = ["firstname", "lastname", "email", "phone", "mobile", "company_name", "sales_contact_id"]
    list_display = ("email", "firstname", "lastname", "phone", "mobile", "company_name", "sales_contact_id", "creation_date", "last_modified")

class ContractAdmin(admin.ModelAdmin):
    fields = ["sales_contact_id", "client_id", "status", "amount", "payment_due"]
    list_display = ("client_id", "sales_contact_id", "status", "amount", "payment_due", "creation_date", "last_modified")

class EventAdmin(admin.ModelAdmin):
    fields = ["client_id", "support_contact_id", "event_status", "attendees", "event_date", "notes"]
    list_display = ("client_id", "support_contact_id", "event_status", "attendees", "event_date", "notes", "creation_date", "last_modified")

admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)

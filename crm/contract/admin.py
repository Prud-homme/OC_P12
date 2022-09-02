from django.contrib import admin

from .models import Contract


class ContractAdmin(admin.ModelAdmin):
    fields = ["sales_contact_id", "client_id", "status", "amount", "payment_due"]
    list_display = (
        "client_id",
        "sales_contact_id",
        "status",
        "amount",
        "payment_due",
        "date_created",
        "date_updated",
    )


admin.site.register(Contract, ContractAdmin)

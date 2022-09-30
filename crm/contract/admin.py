from django.contrib import admin

from .models import Contract


class ContractAdmin(admin.ModelAdmin):
    fields = ["sales_contact", "client", "status", "amount", "payment_due"]
    list_display = (
        "client",
        "sales_contact",
        "status",
        "amount",
        "payment_due",
        "date_created",
        "date_updated",
    )


admin.site.register(Contract, ContractAdmin)

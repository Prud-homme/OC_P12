from django.contrib import admin

from .models import Client


class ClientAdmin(admin.ModelAdmin):
    fields = [
        "firstname",
        "lastname",
        "email",
        "phone",
        "mobile",
        "company_name",
        "sales_contact",
    ]
    list_display = (
        "email",
        "firstname",
        "lastname",
        "phone",
        "mobile",
        "company_name",
        "sales_contact",
        "date_created",
        "date_updated",
    )


admin.site.register(Client, ClientAdmin)

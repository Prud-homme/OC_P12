from django.conf import settings
from django.db import models

from crm.models import TimeStamped


class Contract(TimeStamped):
    sales_contact_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    client_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField(null=True)

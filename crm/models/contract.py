from django.conf import settings
from django.db import models

from .timestamped import TimeStamped


class Contract(TimeStamped):
    sales_contact_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contract_sales_contact",
    )
    client_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contract_client",
    )
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField(null=True)

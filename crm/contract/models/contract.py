from django.conf import settings
from django.db import models
from django.utils import timezone

from crm.client.models import Client


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contract_sales_contact",
    )
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
        related_name="contract_client",
    )
    status = models.BooleanField()
    amount = models.FloatField()
    payment_due = models.DateTimeField(null=True)
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = timezone.now()

        self.date_updated = timezone.now()
        return super(Contract, self).save(*args, **kwargs)

from django.conf import settings
from django.db import models
from django.utils import timezone


class Contract(models.Model):
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
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = timezone.now()

        self.last_modified = timezone.now()
        return super(Contract, self).save(*args, **kwargs)

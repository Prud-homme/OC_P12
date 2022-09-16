from django.conf import settings
from django.db import models
from django.utils import timezone


class Client(models.Model):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250)
    sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_sales_contact",
    )
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = timezone.now()

        self.date_updated = timezone.now()
        return super(Client, self).save(*args, **kwargs)

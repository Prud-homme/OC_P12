import logging
from enum import Enum

from django.conf import settings
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class ClientStatus(Enum):
    """Class that defines the different status of client"""

    POTENTIAL = "potential"
    EXISTING = "existing"

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples representing the possible choices of project types
        """
        return [(key.value, key.name) for key in cls]


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
    obtained_with_sales_contact = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_obtained_with_sales_contact",
        blank=True,
        null=True,
    )
    client_status = models.CharField(max_length=10, choices=ClientStatus.choices())
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = timezone.now()

        self.date_updated = timezone.now()
        super(Client, self).save(*args, **kwargs)
        logger.info("Database has been successfully modified")

from enum import Enum

from django.conf import settings
from django.db import models
from django.utils import timezone

from crm.client.models import Client


class EventStatus(Enum):
    """Class that defines the different status of event"""

    ONGOING = "ongoing"
    ENDED = "ended"

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples representing the possible choices of project types
        """
        return [(key.value, key.name) for key in cls]


class Event(models.Model):
    client_id = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
        related_name="event_client",
    )
    support_contact_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_support_contact",
    )
    event_status = models.CharField(max_length=10, choices=EventStatus.choices())
    attendees = models.PositiveIntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = timezone.now()

        self.date_updated = timezone.now()
        return super(Event, self).save(*args, **kwargs)

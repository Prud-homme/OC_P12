from enum import Enum

from django.conf import settings
from django.db import models

from crm.models import TimeStamped


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


class Event(TimeStamped):
    client_id = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    support_contact_id = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    event_status = models.CharField(max_length=10, choices=EventStatus.choices())
    attendees = models.PositiveIntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()

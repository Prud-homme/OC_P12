from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from crm.event.models import Event
from crm.event.serializers import EventSerializer


class CreateEvent(CreateAPIView):
	pass

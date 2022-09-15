from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from crm.event.models import Event
from crm.event.serializers import EventSerializer


class CreateEvent(CreateAPIView):
	pass

class RetrieveUpdateEvent(RetrieveUpdateAPIView):
	pass

from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from crm.permissions import CustomDjangoModelPermission

from crm.event.models import Event
from crm.event.serializers import EventSerializer


class CreateEvent(CreateAPIView):
    permission_classes = [CustomDjangoModelPermission]

    queryset = Event.objects.all()
    serializer_class = EventSerializer

class RetrieveUpdateEvent(RetrieveUpdateAPIView):
    pass

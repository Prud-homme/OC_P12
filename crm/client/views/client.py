from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from crm.client.models import Client
from crm.client.serializers import ClientSerializer


class CreateClient(CreateAPIView):
	pass

class RetrieveUpdateClient(RetrieveUpdateAPIView):
	pass

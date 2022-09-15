from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from crm.client.models import Client
from crm.client.serializers import ClientSerializer


class CreateClient(CreateAPIView):
	pass
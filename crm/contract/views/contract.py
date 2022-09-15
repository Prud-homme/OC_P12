from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from crm.contract.models import Contract
from crm.contract.serializers import ContractSerializer


class CreateContract(CreateAPIView):
	pass
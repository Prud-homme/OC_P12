from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from crm.contract.models import Contract
from crm.contract.serializers import ContractSerializer


class CreateContract(CreateAPIView):
	pass

class RetrieveUpdateContract(RetrieveUpdateAPIView):
	pass

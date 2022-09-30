import logging

from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from crm.contract.models import Contract
from crm.contract.serializers import ContractSerializer
from crm.exceptions import FilterNotExist
from crm.permissions import CustomDjangoModelPermission

logger = logging.getLogger(__name__)


class ListCreateContract(ListCreateAPIView):
    permission_classes = [CustomDjangoModelPermission]
    serializer_class = ContractSerializer

    def get_queryset(self):

        if self.request.method == "POST":
            queryset = Contract.objects.all()
            return queryset

        query_params = [
            param
            for param in self.request.GET
            if param not in ["email", "lastname", "date", "amount"]
        ]
        if len(query_params) > 0:
            message = f"The filter(s) {', '.join(query_params)} does not exist"
            logger.warning(message)
            raise FilterNotExist

        user = self.request.user
        in_sales_team = (
            get_user_model().objects.filter(pk=user.id, groups__name="sales").exists()
        )
        in_management_team = (
            get_user_model()
            .objects.filter(pk=user.id, groups__name="management")
            .exists()
        )

        if in_management_team:
            queryset = Contract.objects.all()
        elif in_sales_team:
            queryset = Contract.objects.filter(sales_contact__exact=user.id)
        else:
            queryset = Contract.objects.none()
            return queryset

        if lastname := self.request.GET.get("lastname"):
            queryset = queryset.filter(client__lastname__iexact=lastname)

        if email := self.request.GET.get("email"):
            queryset = queryset.filter(client__email__iexact=email)

        if date_created := self.request.GET.get("date"):
            queryset = queryset.filter(date_created__date=date_created)

        if amount := self.request.GET.get("amount"):
            queryset = queryset.filter(amount__exact=amount)

        return queryset


class RetrieveUpdateContract(RetrieveUpdateAPIView):
    permission_classes = [CustomDjangoModelPermission]
    serializer_class = ContractSerializer

    def get_queryset(self):
        user = self.request.user
        in_sales_team = (
            get_user_model().objects.filter(pk=user.id, groups__name="sales").exists()
        )
        in_management_team = (
            get_user_model()
            .objects.filter(pk=user.id, groups__name="management")
            .exists()
        )

        if in_management_team:
            queryset = Contract.objects.all()
        elif in_sales_team:
            queryset = Contract.objects.filter(sales_contact__exact=user.id)
        else:
            queryset = Contract.objects.none()

        return queryset

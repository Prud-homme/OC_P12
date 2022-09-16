from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from crm.contract.models import Contract
from crm.contract.serializers import ContractSerializer
from crm.permissions import CustomDjangoModelPermission


class CreateContract(CreateAPIView):
    permission_classes = [CustomDjangoModelPermission]

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


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
            return Contract.objects.all()
        elif in_sales_team:
            return Contract.objects.filter(sales_contact__exact=user.id)
        else:
            return Contract.objects.none()

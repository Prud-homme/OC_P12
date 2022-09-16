from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from crm.client.models import Client
from crm.client.serializers import ClientSerializer
from crm.permissions import CustomDjangoModelPermission


class CreateClient(CreateAPIView):
    permission_classes = [CustomDjangoModelPermission]

    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class RetrieveUpdateClient(RetrieveUpdateAPIView):
    permission_classes = [CustomDjangoModelPermission]
    serializer_class = ClientSerializer

    def get_queryset(self):
        user = self.request.user
        in_support_team = (
            get_user_model().objects.filter(pk=user.id, groups__name="support").exists()
        )
        in_sales_team = (
            get_user_model().objects.filter(pk=user.id, groups__name="sales").exists()
        )
        in_management_team = (
            get_user_model()
            .objects.filter(pk=user.id, groups__name="management")
            .exists()
        )

        if in_management_team:
            return Client.objects.all()
        elif in_sales_team:
            return Client.objects.filter(sales_contact__exact=user.id)
        elif in_support_team:
            return Client.objects.filter(event_client__support_contact__exact=user.id)
        else:
            return Client.objects.none()

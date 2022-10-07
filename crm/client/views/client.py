import logging

from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from crm.client.models import Client
from crm.client.serializers import ClientSerializer
from crm.exceptions import FilterNotExist
from crm.permissions import CustomDjangoModelPermission

logger = logging.getLogger(__name__)


class ListCreateClient(ListCreateAPIView):
    permission_classes = [CustomDjangoModelPermission]
    serializer_class = ClientSerializer

    def get_queryset(self):

        if self.request.method == "POST":
            queryset = Client.objects.all()
            return queryset

        query_params = [
            param for param in self.request.GET if param not in ["email", "lastname"]
        ]
        if len(query_params) > 0:
            message = f"The filter(s) {', '.join(query_params)} does not exist"
            logger.warning(message)
            raise FilterNotExist

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
            queryset = Client.objects.all()
        elif in_sales_team:
            queryset = Client.objects.filter(sales_contact__exact=user.id)
        elif in_support_team:
            queryset = Client.objects.filter(
                event_client__support_contact__exact=user.id
            )
        else:
            queryset = Client.objects.none()
            return queryset

        if email := self.request.GET.get("email"):
            queryset = queryset.filter(email__iexact=email)

        if lastname := self.request.GET.get("lastname"):
            queryset = queryset.filter(lastname__iexact=lastname)

        return queryset.distinct()


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
            queryset = Client.objects.all()
        elif in_sales_team:
            queryset = Client.objects.filter(sales_contact__exact=user.id)
        elif in_support_team:
            queryset = Client.objects.filter(
                event_client__support_contact__exact=user.id
            )
        else:
            queryset = Client.objects.none()

        return queryset.distinct()

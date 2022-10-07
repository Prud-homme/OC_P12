import logging

from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from crm.event.models import Event
from crm.event.serializers import EventSerializer
from crm.exceptions import FilterNotExist
from crm.permissions import CustomDjangoModelPermission

logger = logging.getLogger(__name__)


class ListCreateEvent(ListCreateAPIView):
    permission_classes = [CustomDjangoModelPermission]
    serializer_class = EventSerializer

    def get_queryset(self):

        if self.request.method == "POST":
            queryset = Event.objects.all()
            return queryset

        query_params = [
            param
            for param in self.request.GET
            if param not in ["email", "lastname", "date"]
        ]
        if len(query_params) > 0:
            message = f"The filter(s) {', '.join(query_params)} does not exist"
            logger.warning(message)
            raise FilterNotExist

        user = self.request.user
        in_support_team = (
            get_user_model().objects.filter(pk=user.id, groups__name="support").exists()
        )
        in_management_team = (
            get_user_model()
            .objects.filter(pk=user.id, groups__name="management")
            .exists()
        )

        if in_management_team:
            queryset = Event.objects.all()
        elif in_support_team:
            queryset = Event.objects.filter(support_contact__exact=user.id)
        else:
            queryset = Event.objects.none()
            return queryset

        if lastname := self.request.GET.get("lastname"):
            queryset = queryset.filter(client__lastname__iexact=lastname)

        if email := self.request.GET.get("email"):
            queryset = queryset.filter(client__email__iexact=email)

        if event_date := self.request.GET.get("date"):
            queryset = queryset.filter(event_date__date=event_date)

        return queryset


class RetrieveUpdateEvent(RetrieveUpdateAPIView):
    permission_classes = [CustomDjangoModelPermission]
    serializer_class = EventSerializer

    def get_queryset(self):
        user = self.request.user
        in_support_team = (
            get_user_model().objects.filter(pk=user.id, groups__name="support").exists()
        )
        in_management_team = (
            get_user_model()
            .objects.filter(pk=user.id, groups__name="management")
            .exists()
        )

        if in_management_team:
            queryset = Event.objects.all()
        elif in_support_team:
            queryset = Event.objects.filter(support_contact__exact=user.id)
        else:
            queryset = Event.objects.none()

        return queryset

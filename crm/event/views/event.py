from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from crm.event.models import Event
from crm.event.serializers import EventSerializer
from crm.permissions import CustomDjangoModelPermission


class CreateEvent(CreateAPIView):
    permission_classes = [CustomDjangoModelPermission]

    queryset = Event.objects.all()
    serializer_class = EventSerializer


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
            return Event.objects.all()
        elif in_support_team:
            return Event.objects.filter(support_contact__exact=user.id)
        else:
            return Event.objects.none()

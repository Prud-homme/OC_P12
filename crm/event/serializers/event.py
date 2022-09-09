from rest_framework.serializers import ModelSerializer

from crm.event.models import Event


class EventSerializer(ModelSerializer):
    """"""

    class Meta:
        model = Event
        fields = [field.name for field in Event._meta.get_fields() if field.name not in ("date_created", "date_updated")]


from rest_framework.serializers import ModelSerializer

from crm.client.models import Client


class ClientSerializer(ModelSerializer):
    """"""

    class Meta:
        model = Client
        fields = [field.name for field in Client._meta.get_fields() if field.name not in ("date_created", "date_updated")]


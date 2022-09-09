from rest_framework.serializers import ModelSerializer

from crm.contract.models import Contract


class ContractSerializer(ModelSerializer):
    """"""

    class Meta:
        model = Contract
        fields = [field.name for field in Contract._meta.get_fields() if field.name not in ("date_created", "date_updated")]


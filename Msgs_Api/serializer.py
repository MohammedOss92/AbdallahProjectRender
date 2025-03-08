from rest_framework import serializers
from Msgs_Api.models import * 

class MsgsTypesSerializer (serializers.ModelSerializer):
    class Meta:
        model = MeesageType
        fields = '__all__'


class MessegasSerializer (serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'



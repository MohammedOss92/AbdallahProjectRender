from rest_framework import serializers
from Nokat_api.models import * 





class NokatTypesSerializer (serializers.ModelSerializer):
    class Meta:
        model = NokatType
        fields = '__all__'


class SnippetsDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Nokat
    fields = '__all__'    


class SnippetsDetailSerializers(serializers.ModelSerializer):

  class Meta:
    model = ImagesNokat
    fields = '__all__'
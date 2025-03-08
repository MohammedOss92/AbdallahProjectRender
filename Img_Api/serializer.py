from rest_framework import serializers
from Img_Api.models import * 

class ImgsTypesSerializer (serializers.ModelSerializer):
    class Meta:
        model = ImageType
        fields = '__all__'


class SnippetsDetailSerializer(serializers.ModelSerializer):

  class Meta:
    model = Imgs
    fields = ['id', 'ID_Type', 'new_img','image_url','my_time_auto']
    # fields = ['id', 'ID_Type', 'pic', 'new_img','image_url']



#class ImgsSerializer (serializers.ModelSerializer):
#    class Meta:
#        model = Images
#        fields = '__all__'



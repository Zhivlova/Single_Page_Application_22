from typing import Type
from rest_framework.serializers import HyperlinkedModelSerializer
from .models import Item


class ItemModelSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

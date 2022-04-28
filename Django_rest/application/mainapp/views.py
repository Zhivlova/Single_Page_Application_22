from rest_framework.viewsets import ModelViewSet
from .models import Item
from .serializers import ItemModelSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemModelSerializer

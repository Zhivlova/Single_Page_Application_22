from django.db import models
from uuid import uuid4


class Item(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=64)
    date = models.DateField(null=True)
    quantity = models.PositiveIntegerField(null=False)
    distance = models.PositiveIntegerField(null=False)

from django.db.models import CharField

from apps.shared.models import BaseModel


class Product(BaseModel):
    name = CharField(max_length=256)

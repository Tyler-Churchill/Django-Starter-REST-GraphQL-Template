import factory
from apps.products.models import Product

from apps.testing import BaseModelFactory


class ProductFactory(BaseModelFactory):
    name = factory.Sequence(lambda n: "Product %s" % n)

    class Meta:
        model = Product

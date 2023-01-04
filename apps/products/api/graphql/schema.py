import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from apps.products.models import Product


class ProductNode(DjangoObjectType):
    id = graphene.ID(source="id", required=True)

    class Meta:
        model = Product
        fields = ("id", "name")
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
        }
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    all_products = DjangoFilterConnectionField(ProductNode)


schema = graphene.Schema(query=Query)

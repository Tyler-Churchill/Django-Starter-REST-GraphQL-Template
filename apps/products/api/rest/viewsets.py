from rest_framework import permissions, viewsets

from apps.products.api.rest.serializers import (
    PublicProductSerializer,
    UserProductSerializer,
)
from apps.products.models import Product


class PublicProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.order_by("created_at").all()
    serializer_class = PublicProductSerializer
    permission_classes = [permissions.AllowAny]


class UserBasedProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by("created_at").all()
    serializer_class = UserProductSerializer
    permission_classes = [permissions.IsAuthenticated]

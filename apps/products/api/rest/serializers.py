from rest_framework import serializers

from apps.products.models import Product


class PublicProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "created_at")


class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

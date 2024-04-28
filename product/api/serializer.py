from rest_framework import serializers

from product.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Product
        fields = "__all__"

class ProductCreateSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Product
        fields = ["id", "title", "slug", "text", "created_at", "category"]

class CategorySerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]
        
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView, 
    DestroyAPIView
)

from product.api.serializer import (
    ProductSerializer,
    ProductCreateSerializer, 
    CategorySerializer
)

from product.models import Product, Category


class ProductFilterAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @swagger_auto_schema(
            tags=['Product'], 
            operation_description='List all or filtered products',
            manual_parameters=[
                openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimum price", type=openapi.TYPE_NUMBER),
                openapi.Parameter('max_price', openapi.IN_QUERY, description="Maximum price", type=openapi.TYPE_NUMBER),
            ],
            responses={200: ProductSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            'count': count,
            'results': serializer.data
        }
        return Response(data)
    
    def get_queryset(self):
        queryset = Product.objects.all()
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class ProductRetrieveView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
            tags=['Product'], 
            operation_description='Get product with id',
            responses={200: ProductSerializer(many=False)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductDeleteView(DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
            tags=['Product'], 
            operation_description='Delete product with id')
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductCreateView(CreateAPIView):
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()

    @swagger_auto_schema(
            tags=['Product'], 
            operation_description='Create a product',
            responses={200: ProductSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @swagger_auto_schema(
            tags=['Category'], 
            operation_description='List all categories',
            responses={200: CategorySerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryRetrieveView(RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
            tags=['Category'],  
            operation_description='Get category with id',
            responses={200: CategorySerializer(many=False)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryDeleteView(DestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"

    @swagger_auto_schema(
            tags=['Category'], 
            operation_description='Delete category with id')
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CategoryCreateView(CreateAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @swagger_auto_schema(
            tags=['Category'],  
            operation_description='Create a category',
            responses={200: CategorySerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Category
from .permissions import IsAuthenticatedCustom
from .producer import publish


class CreateProductApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            publish('product_created', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        product = Product.objects.all()

        if not product:
            return Response({"error": "product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, many=True)
        publish('list_of_products', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCategoryApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            publish('created_category', serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category = Category.objects.all()

        if not category:
            return Response({"error": "category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, many=True)
        publish('list_of_category', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)



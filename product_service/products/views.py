from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializers import CategorySerializer, ProductListSerializer, ProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Category
from .permissions import IsAuthenticatedCustom


@api_view(['POST'])
@permission_classes([IsAuthenticatedCustom])
def create_product(request):

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user_id=request.user_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        product = Product.objects.all()

        if not product:
            return Response({"error": "product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductListSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCategoryApiView(APIView):
    permission_classes = [IsAuthenticatedCustom]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category = Category.objects.all()

        if not category:
            return Response({"error": "category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetProductAPiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)

        if not product:
            return Response({"error": "Product Not Found.!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)

        return Response(serializer.data)

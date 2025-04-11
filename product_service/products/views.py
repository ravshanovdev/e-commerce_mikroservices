import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializers import CategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Category
from .permissions import IsAuthenticatedCustom
from django.http import HttpRequest
from rest_framework.authentication import TokenAuthentication

AUTH_SERVICE_URL = "http://localhost:8000/accounts/api/token/verify/"


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_product(request):
    auth_header = request.headers.get("Authorization", "")

    if auth_header.startswith("Bearer "):
        token = auth_header.split(' ')[1]
    else:
        token = None
    print(token)
    print('token topilmadi')
    if token is None:
        return Response({"detail": "Token topilmadi"}, status=status.HTTP_401_UNAUTHORIZED)

    response = requests.post(AUTH_SERVICE_URL, data={"token": token})

    if response.status_code != 200:
        return Response({"detail": "Token noto'g'ri yoki foydalanuvchi mavjud emas"},
                        status=status.HTTP_401_UNAUTHORIZED)

    serializer = ProductSerializer(data=request.data)
    print('token')
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        product = Product.objects.all()

        if not product:
            return Response({"error": "product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCategoryApiView(APIView):
    permission_classes = [IsAuthenticated]

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



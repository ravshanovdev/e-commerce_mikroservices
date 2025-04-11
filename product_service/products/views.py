import jwt
from django.conf import settings
import requests
from config.utils import decode_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializers import CategorySerializer, ProductListSerializer, ProductSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Category
from .permissions import IsAuthenticatedCustom
from django.http import HttpRequest
from rest_framework.authentication import TokenAuthentication

AUTH_SERVICE_URL = "http://localhost:8000/accounts/api/token/verify/"


# def decode_token(token):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         return payload.get("user_id")
#     except jwt.ExpiredSignatureError:
#         return None
#     except jwt.InvalidTokenError:
#         return None


@api_view(['POST'])
@permission_classes([IsAuthenticatedCustom])
def create_product(request):
    token = request.headers.get("Authorization", "").replace('Bearer ', '')

    if token is None:
        return Response({"detail": "Token topilmadi"}, status=status.HTTP_401_UNAUTHORIZED)

    response = requests.post(AUTH_SERVICE_URL, data={"token": token})

    if response.status_code != 200:
        return Response({"detail": "Token noto'g'ri yoki foydalanuvchi mavjud emas"},
                        status=status.HTTP_401_UNAUTHORIZED)

    user_id = decode_token(token)
    if not user_id:
        return Response({"detail": "Foydalanuvchi aniqlanmadi"}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data.copy()
    data['user_id'] = user_id

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user_id=user_id)

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
    # permission_classes = [IsAuthenticated]

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



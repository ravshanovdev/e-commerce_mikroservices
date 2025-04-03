from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from consumer import send_user_created_event, send_token_event

User = get_user_model()


class UserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            send_user_created_event({
                "id": user.id,
                "username": user.username,
                "email": user.email,
            })

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Token olish
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Token olish muvaffaqiyatli bo'lsa, RabbitMQ'ga xabar yuborish
            data = response.data
            send_token_event({
                "username": request.data['username'],
                "token": data['access']
            })
            print(data['access'])
        return response






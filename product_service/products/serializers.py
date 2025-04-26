from rest_framework import serializers
from .models import Product, Category
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'user_id', 'name', 'description', 'price', 'stock', 'category']


# bu ProductListSerializer ni takomilashtirish kerak yani user_id ga nafaqat
# user_id ni balki userning boshqa datalarini ham chiqarish kerak. balki buni front qilar yanayam koramiz

class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'user_id', 'name', 'description', 'price', 'stock', 'category']

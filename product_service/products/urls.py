from django.urls import path
from .views import create_product, CreateCategoryApiView, ProductListApiView, CategoryListApiView


urlpatterns = [
    path('create_product/', create_product, ),
    path('create_category/', CreateCategoryApiView.as_view(), ),
    path('list_product/', ProductListApiView.as_view(), ),
    path('list_category/', CategoryListApiView.as_view(), ),



]


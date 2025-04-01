from django.urls import path
from .views import CreateProductApiView, CreateCategoryApiView, ProductListApiView, CategoryListApiView


urlpatterns = [
    path('create_product/', CreateProductApiView.as_view(), ),
    path('create_category/', CreateCategoryApiView.as_view(), ),
    path('list_product/', ProductListApiView.as_view(), ),
    path('list_category/', CategoryListApiView.as_view(), ),



]


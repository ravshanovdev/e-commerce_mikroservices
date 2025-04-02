from django.urls import path
from .views import UserRegister, CustomTokenObtainPairView, VerifyTokenView, ProductApiView, CategoryApiView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify_token/', TokenRefreshView.as_view(), name='verify-token'),

    path('list/product/', ProductApiView.as_view(), ),
    path('list/category/', CategoryApiView.as_view(), ),


]



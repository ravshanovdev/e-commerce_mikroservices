from django.urls import path
from .views import CreateSessionPaymentApiView


urlpatterns = [
    path('create_payment/<int:product_id>/', CreateSessionPaymentApiView.as_view(), ),

]


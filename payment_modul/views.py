import stripe
import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


class CreateSessionPaymentApiView(APIView):
    def post(self, request, product_id):
        try:
            response = requests.get(f'http://localhost:8080/product/get_product/{product_id}/')
            product = response.json()

            if not product:
                return Response({"error": "Product Not Found"}, status=status.HTTP_404_NOT_FOUND)

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],

                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product['name'],
                        },
                        'unit_amount': int(product['price'] * 100),  # Stripe = cent
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
            )

            return Response({'checkout_url': session.url})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


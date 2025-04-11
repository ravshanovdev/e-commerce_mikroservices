from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from config.utils import verify_jwt_token, decode_token
from rest_framework.response import Response
import requests
from rest_framework import status

AUTH_SERVICE_URL = "http://localhost:8000/accounts/api/token/verify/"


class IsAuthenticatedCustom(BasePermission):

    def has_permission(self, request, view):
        token = request.headers.get("Authorization", "").replace('Bearer ', '')
        if not token:
            raise AuthenticationFailed("Token required")

        try:
            if token is None:
                return Response({"detail": "Token topilmadi"}, status=status.HTTP_401_UNAUTHORIZED)
            response = requests.post(AUTH_SERVICE_URL, data={"token": token})

            if response.status_code != 200:
                return Response({"detail": "Token noto'g'ri yoki foydalanuvchi mavjud emas"},
                                status=status.HTTP_401_UNAUTHORIZED)
            return token
        except Exception as e:
            return Response({"error": str(e)})




#


# @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# def create_product(request):
#     token = request.headers.get("Authorization", "").replace('Bearer ', '')
#
#     if token is None:
#         return Response({"detail": "Token topilmadi"}, status=status.HTTP_401_UNAUTHORIZED)
#
#     response = requests.post(AUTH_SERVICE_URL, data={"token": token})
#
#     if response.status_code != 200:
#         return Response({"detail": "Token noto'g'ri yoki foydalanuvchi mavjud emas"},
#                         status=status.HTTP_401_UNAUTHORIZED)
#
#     user_id = decode_token(token)
#     if not user_id:
#         return Response({"detail": "Foydalanuvchi aniqlanmadi"}, status=status.HTTP_401_UNAUTHORIZED)
#
#     data = request.data.copy()
#     data['user_id'] = user_id
#
#     serializer = ProductSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(user_id=user_id)
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


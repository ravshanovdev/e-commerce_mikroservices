from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from config.utils import verify_jwt_token, decode_token
from rest_framework.response import Response
import requests
from rest_framework import status

AUTH_SERVICE_URL = "http://auth-service:8000/accounts/api/token/verify/"


class IsAuthenticatedCustom(BasePermission):

    def has_permission(self, request, view):
        token = request.headers.get("Authorization", "").replace('Bearer ', '')

        if not token:
            raise AuthenticationFailed("Token topilmadi")

        response = requests.post(AUTH_SERVICE_URL, data={'token': token})

        if response.status_code != 200:
            raise AuthenticationFailed("Token incorrect or user doesn't exist.!")

        user_id = decode_token(token)
        if not user_id:
            raise AuthenticationFailed('user not found.!')

        request.user_id = user_id

        return True



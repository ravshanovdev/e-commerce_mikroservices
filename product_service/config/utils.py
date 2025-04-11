import requests
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

AUTH_SERVICE_URL = "http://0.0.0.0:8000/account/verify_token/"  # Auth servising JWT tokenni tekshirish endpointi


def verify_jwt_token(token):
    """Auth Service ga so‘rov yuborib, tokenni tekshiradi"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(AUTH_SERVICE_URL, headers=headers)
        if response.status_code == 200:
            return response.json()  # Foydalanuvchi ma'lumotlari
        raise AuthenticationFailed("Invalid token")
    except requests.RequestException:
        raise AuthenticationFailed("Auth Service not available")


def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

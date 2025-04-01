from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from config.utils import verify_jwt_token


class IsAuthenticatedCustom(BasePermission):

    def has_permission(self, request, view):
        token = request.headers.get("Authorization")
        if not token:
            raise AuthenticationFailed("Token required")

        try:
            # token = token.split(" ")[1]
            user = verify_jwt_token(token)
            request.user = user
            return True
        except AuthenticationFailed:
            return False

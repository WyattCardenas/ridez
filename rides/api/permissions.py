from rest_framework.permissions import BasePermission

from rides.models import Roles


class IsAdmin(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.role == Roles.ADMIN)

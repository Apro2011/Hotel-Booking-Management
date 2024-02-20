from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status


class IsAuthenticated(IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    message = {
        "data": [],
        "errors": ["This user is not authenticated!"],
        "status": "Failure",
    }

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdminUser(IsAdminUser):
    """
    Allows access only to admin users.
    """

    message = {
        "data": [],
        "errors": ["Only admin users have permission to view this!"],
        "status": "Failure",
    }

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

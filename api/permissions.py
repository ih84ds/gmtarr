from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated

class IsAdminUserOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
            ( request.method in SAFE_METHODS ) or
            ( request.user and is_authenticated(request.user) and request.user.is_staff )
        )

class IsAdminUserOrReadOnlyAuthenticated(BasePermission):
    """
    The request is authenticated as an admin user, or is a read-only request.
    No access for anonymous users.
    """

    def has_permission(self, request, view):
        return request.user and is_authenticated(request.user) and (
            ( request.method in SAFE_METHODS ) or
            ( request.user.is_staff )
        )

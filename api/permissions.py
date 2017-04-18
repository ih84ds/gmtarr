from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.compat import is_authenticated

class IsAdminUserOrMatchPlayerOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin user or player assigned to a Match.
    """

    def is_match_player(self, user, obj):
        home_user = obj.home_player and obj.home_player.user
        if home_user == user:
            return True
        visitor_user = obj.visitor_player and obj.visitor_player.user
        if visitor_user == user:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            # everyone has read-only access
            return True
        user = request.user
        if not is_authenticated(user):
            return False
        if user.is_staff:
            return True
        if self.is_match_player(user, obj):
            return True
        return False

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

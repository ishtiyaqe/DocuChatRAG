from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    """
    Allows access only to the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            # read allowed only to owner
            return obj.owner == request.user
        return obj.owner == request.user

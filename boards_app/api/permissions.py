from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated

    
class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user in obj.members.all() or request.user.id == obj.owner_id)
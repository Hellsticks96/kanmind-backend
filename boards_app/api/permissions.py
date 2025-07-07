from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated
from tasks_app.models import Task

    
class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Task) and request.method == "PATCH":
            board = obj.board
            return bool(request.user in board.members.all() or request.user == board.owner)
        return bool(request.user in obj.members.all() or request.user.id == obj.owner.id)
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.id == obj.owner.id)
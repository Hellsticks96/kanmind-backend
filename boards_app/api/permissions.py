from rest_framework.permissions import BasePermission
from tasks_app.models import Task


    
class IsOwnerOrMember(BasePermission):
    message = "You have to be an owner or member of a board to perform this action"
    def has_object_permission(self, request, view, obj):
        print("using isownerormember")
        if isinstance(obj, Task) and request.method == "PATCH":
            board = obj.board
            return bool(request.user in board.members.all() or request.user == board.owner)
        return bool(request.user in obj.members.all() or request.user.id == obj.owner.id)
    
class IsOwnerOrMemberList(BasePermission):
    message = "You have to be an owner or member of a board to perform this action"
    def has_permission(self, request, view):
        task_id = view.kwargs.get("pk")
        print("task id", task_id)
        try:
            task = Task.objects.get(id=task_id)
            print("task", task)
        except Task.DoesNotExist:
            return True
        
        board = task.board
        return bool(request.user == board.owner or request.user in board.members.all())
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.id == obj.owner.id)
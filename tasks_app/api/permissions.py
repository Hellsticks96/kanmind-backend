from rest_framework.permissions import BasePermission, SAFE_METHODS
from boards_app.models import Board

class IsAssigneeOrReviewer(BasePermission):
    message = "You have to be the assignee or the reviewer of a task to view the tasks"
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            board_id = request.data.get("board")
            if not board_id:
                return False

            board = Board.objects.get(pk=board_id)
            if not board:
                return False

            return bool(request.user in board.members.all() or request.user.id == board.owner.id)
        if request.method == "GET":
            print("getting boards")
            return bool(request.user == obj.assignee or request.user == obj.reviewer)

class IsTaskCreatorOrBoardOwner(BasePermission):
    message = "You have to be the owner of the board or the creator of the task to be able to delete it!"
    def has_object_permission(self, request, view, obj):
        board_id = obj.board.owner.id
        return bool(request.user == obj.task_author or request.user == obj.board.owner)
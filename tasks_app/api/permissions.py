from rest_framework.permissions import BasePermission, SAFE_METHODS
from boards_app.models import Board

class IsAssigneeOrReviewer(BasePermission):
    message = "You have to be a member or the owner of a board to add a task"
    def has_permission(self, request, view):
        if request.method == "POST":
            board_id = request.data.get("board")
            if not board_id:
                return False

            board = Board.objects.get(pk=board_id)
            if not board:
                return False

            return bool(request.user in board.members.all() or request.user.id == board.owner_id)
from rest_framework.permissions import BasePermission, SAFE_METHODS
from boards_app.models import Board
from tasks_app.models import Task
from django.db.models import Q
from django.http import Http404

class IsAssigneeOrReviewer(BasePermission):
    message = "You have to be the assignee or the reviewer of a task to view the tasks"
    def has_permission(self, request, view):
         if request.method == "GET":
              return bool(Task.objects.filter(Q(assignee=request.user) | Q(reviewer=request.user)))
    def has_object_permission(self, request, view, obj):
            return bool(request.user == obj.assignee or request.user == obj.reviewer)

class IsTaskCreatorOrBoardOwner(BasePermission):
    message = "You have to be the owner of the board or the creator of the task to be able to delete it!"
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.task_author or request.user == obj.board.owner)
    
class CanCreateTaskOnBoard(BasePermission):
     message = "You need to be the owner or a member of a board to create a task"
     def has_permission(self, request, view):
          board_id = request.data.get("board")
          try:
            board = Board.objects.get(pk=board_id)
          except Board.DoesNotExist:
            raise Http404("No Board found with given id")
          return bool(request.user == board.owner or request.user in board.members.all())
     
class IsCommentAuthor(BasePermission):
    message = "Only the author of a comment can delete it"
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.author)
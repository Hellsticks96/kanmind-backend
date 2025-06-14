from rest_framework import generics
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from .permissions import IsAssigneeOrReviewer
from django.utils.timezone import now


class TasksList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAssigneeOrReviewer]

class ReviewerTasksList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(reviewer_id=self.request.user)
    
class AssigneeTasksList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(assignee_id=self.request.user)
    
class TasksSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class CommentsList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs["pk"])

    def perform_create(self, serializer):
        task = Task.objects.get(id=self.kwargs["pk"])
        serializer.save(task=task, author=self.request.user, created_at=now().date())

class CommentDelete(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs["task_id"], id=self.kwargs["comment_id"])
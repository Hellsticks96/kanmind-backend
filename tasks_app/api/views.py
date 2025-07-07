from rest_framework import generics
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from .permissions import IsAssigneeOrReviewer, IsTaskCreatorOrBoardOwner
from django.utils.timezone import now
from boards_app.api.permissions import IsOwnerOrMember
from rest_framework.permissions import IsAuthenticated


class TasksList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAssigneeOrReviewer]

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(task_author=author)

class ReviewerTasksList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes=[IsAssigneeOrReviewer]
    
    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)
    
class AssigneeTasksList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAssigneeOrReviewer]
    
    def get_queryset(self):
        return Task.objects.filter(assignee_id=self.request.user)
    
class TasksSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsTaskCreatorOrBoardOwner]
            return [permission() for permission in permission_classes]
        if self.request.method == "PATCH":
            permission_classes = [IsAuthenticated, IsOwnerOrMember]
            return [permission() for permission in permission_classes]

class CommentsList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrMember]
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
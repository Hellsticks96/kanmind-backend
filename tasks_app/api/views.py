from rest_framework import generics
from tasks_app.models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from .permissions import IsAssigneeOrReviewer, IsTaskCreatorOrBoardOwner, CanCreateTaskOnBoard, IsCommentAuthor
from django.utils.timezone import now
from boards_app.api.permissions import IsOwnerOrMember, IsOwnerOrMemberList
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class TasksList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated, CanCreateTaskOnBoard]
        else:
            permission_classes = [IsAuthenticated, IsAssigneeOrReviewer]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        print("hello")
        author = self.request.user
        serializer.save(task_author=author)

class ReviewerTasksList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes=[IsAuthenticated, IsAssigneeOrReviewer]

    
class AssigneeTasksList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAssigneeOrReviewer]
    
    
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
    permission_classes = [IsAuthenticated, IsOwnerOrMemberList]
    
    def get_queryset(self):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        return Comment.objects.filter(task=task)

    def perform_create(self, serializer):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        serializer.save(task=task, author=self.request.user, created_at=now().date())

class CommentDelete(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_id"
    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs["task_id"], id=self.kwargs["comment_id"])
from django.urls import path
from .views import TasksList, ReviewerTasksList, AssigneeTasksList, TasksSingleView, CommentsList, CommentDelete

urlpatterns = [
    path("tasks/", TasksList.as_view(), name='task-detail'),
    path("tasks/reviewing/", ReviewerTasksList.as_view(), name="reviewer-detail"),
    path("tasks/assigned-to-me/", AssigneeTasksList.as_view(), name="asignee-detail"),
    path("tasks/<int:pk>/", TasksSingleView.as_view(), name="single-detail"),
    path("tasks/<int:pk>/comments/", CommentsList.as_view(), name="comments-detail"),
    path("tasks/<int:task_id>/comments/<int:comment_id>/", CommentDelete.as_view(), name="delete-detail")
]
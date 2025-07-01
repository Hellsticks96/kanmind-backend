from django.db import models
from django.contrib.auth.models import User
from boards_app.models import Board

# Create your models here.

class Choices:
    status = (
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("review", "review"),
        ("done", "done")
    )

    prio = (
        ("low", "low"),
        ("medium", "medium"),
        ("high", "high")
    )

class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(choices=Choices.status, default="To Do", max_length=20)
    priority = models.CharField(choices=Choices.prio, default="Medium", max_length=20)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="asigned_tasks", null=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewed_tasks", null=True)
    due_date = models.DateTimeField()
    task_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_author", null=True)

class Comment(models.Model):
    created_at = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments", null=True)
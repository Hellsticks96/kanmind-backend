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
        ("lmow", "lmow"),
        ("medium", "medium"),
        ("high", "high")
    )

class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(choices=Choices.status, default="To Do", max_length=20)
    priority = models.CharField(choices=Choices.prio, default="Medium", max_length=20)
    assignee_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="asignee_id", null=True)
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer_id", null=True)
    due_date = models.DateTimeField()

class Comment(models.Model):
    created_at = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments", null=True)
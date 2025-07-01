from rest_framework import serializers
from boards_app.models import Board
from django.contrib.auth.models import User
from tasks_app.models import Task
from tasks_app.api.serializers import TaskSerializer

class UserShortSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]

class TaskSerializer(serializers.ModelSerializer):
    assignee = UserShortSerializer(read_only=True)
    reviewer = UserShortSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id", "title", "description", "status", "priority",
            "assignee", "reviewer", "due_date", "comments_count"
        ]

    def get_comments_count(self, obj):
        return obj.comments.count() if hasattr(obj, 'comments') else 0

class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )
        
    class Meta:
        model = Board
        exclude = []

    def get_member_count(self, obj):
        return obj.members.count()
    
class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserShortSerializer(read_only=True, many=True)
    tasks = TaskSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]

class BoardPatchResponseSerializer(serializers.ModelSerializer):
    owner_data = UserShortSerializer(source="owner", read_only=True)
    members_data = UserShortSerializer(source="members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members_data"]
    
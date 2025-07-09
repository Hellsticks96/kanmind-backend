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
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = User.objects.all(),
        write_only=True
    )
    member_count = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()
        
    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "members", "ticket_count", "tasks_to_do_count", "tasks_high_prio_count", "owner_id"]

    def get_member_count(self, obj):
        return obj.members.count()
    
    def create(self, validated_data):
        members_data = validated_data.pop("members")
        board = Board.objects.create(**validated_data)
        board.members.set(members_data)
        return board
    
    def get_owner_id(self, obj):
        return obj.owner.id
    
class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserShortSerializer(read_only=True, many=True)
    tasks = TaskSerializer(read_only=True, many=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]

class BoardPatchResponseSerializer(serializers.ModelSerializer):
    owner_data = UserShortSerializer(source="owner", read_only=True)
    members_data = UserShortSerializer(source="members", many=True, read_only=True)
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset = User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members_data", "members"]

    def update(self, instance, validated_data):
        members_data = validated_data.pop("members", None)
        print("members",members_data)
        updated_instance = super().update(instance, validated_data)
        if members_data is not None:
            updated_instance.members.set(members_data)
        return updated_instance
    
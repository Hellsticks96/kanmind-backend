from rest_framework import serializers
from tasks_app.models import Task, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSummarySerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return obj.username


class TaskSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    comments = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), write_only=True, many=True)

    assignee = UserSummarySerializer(source='assignee_id', read_only=True)
    reviewer = UserSummarySerializer(source='reviewer_id', read_only=True)
    comments = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        return obj.members.count()

    class Meta:
        model = Task
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "author", "created_at", "content"]
        read_only_fields = ("author", "created_at")

    def get_author(self, obj):
        return obj.author.username
from rest_framework import serializers
from boards_app.models import Board
from django.contrib.auth.models import User

class BoardSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )

    member_count = serializers.SerializerMethodField()
        
    class Meta:
        model = Board
        exclude = []

    def get_member_count(self, obj):
        return obj.members.count()
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]
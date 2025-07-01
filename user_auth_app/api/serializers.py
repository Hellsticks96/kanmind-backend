import uuid
from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'fullname', 'bio', 'location']

class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        pw = self.validated_data['password']
        rep_pw = self.validated_data['repeated_password']
        fullname = self.validated_data['fullname']

        if pw != rep_pw:
            raise serializers.ValidationError({'error': "Passwords don't match"})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already registered'})
        username = str(uuid.uuid4())[:30]
        account = User(email=self.validated_data['email'], username=fullname)
        account.set_password(pw)
        account.save()
        UserProfile.objects.create(user=account, fullname=self.validated_data['fullname'])
        return account

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
    
        if email and password:
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError({"detail": ["Invalid email or password."]})
    
            user = authenticate(username=user_obj.username, password=password)
    
            if not user:
                raise serializers.ValidationError({"detail": ["Invalid email or password."]})
        else:
            raise serializers.ValidationError({"detail": ["Must include 'email' and 'password'."]})
    
        attrs['user'] = user
        return attrs
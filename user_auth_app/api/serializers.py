from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']

class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only':True
            }
        }

    def save(self):
            pw = self.validated_data['password']
            rep_pw = self.validated_data['repeated_password']

            if pw != rep_pw:
                raise serializers.ValidationError({'error': "passwords don't match"})
            if User.objects.filter(email=self._validated_data['email']).exists():
                raise serializers.ValidationError({'error': 'email already registered'})

            account = User(email=self.validated_data['email'], username=self.validated_data['fullname'])
            account.set_password(pw)
            account.save()
            return account
    
class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError({"detail": _("Invalid email or password.")}, code='authorization')
        else:
            raise serializers.ValidationError({"detail": _("Must include 'email' and 'password'.")}, code='authorization')

        attrs['user'] = user
        return attrs
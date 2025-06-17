from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import RegistrationSerializer, UserProfileSerializer, CustomAuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        statuscode = status.HTTP_201_CREATED
        if serializer.is_valid():
            saved_account = serializer.save()
            profile = UserProfile.objects.get(user=saved_account)
            token, _ = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'fullname': profile.fullname,
                'email': saved_account.email,
                'user_id': saved_account.pk
            }
        else:
            data = serializer.errors
            statuscode = status.HTTP_400_BAD_REQUEST
        return Response(data, status=statuscode)

class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomAuthTokenSerializer(data=request.data)
        data = {}
        statuscode = status.HTTP_200_OK
        if serializer.is_valid():
            user = serializer.validated_data['user']
            profile = UserProfile.objects.get(user=user)
            token, _ = Token.objects.get_or_create(user=user)

            data = {
                'token': token.key,
                'fullname': profile.fullname,
                'email': user.email,
                'user_id': user.pk
            }
        else:
            data = serializer.errors
            statuscode = status.HTTP_400_BAD_REQUEST
        return Response(data, status=statuscode)
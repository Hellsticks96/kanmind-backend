from rest_framework import generics
from boards_app.models import Board
from .serializers import BoardSerializer, BoardDetailSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrMember
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from rest_framework import status
from rest_framework.response import Response

class BoardsList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrMember]

    def perform_create(self, serializer):
        owner_id = self.request.user.id
        serializer.save(owner_id=owner_id)
    
    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(members=user) | Q(owner_id=user.id))
    

class SingleBoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer

class EmailCheck(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        email = request.GET.get("email")
        if not email:
            return JsonResponse({"error": "Email query parameter is required"}, status=400)

        try:
            user = User.objects.get(email=email)
            data = {
                "id": user.id,
                "email": user.email,
                "fullname": user.username
            }
            return JsonResponse(data)
        except User.DoesNotExist:
            raise Http404("No user with provided email found")
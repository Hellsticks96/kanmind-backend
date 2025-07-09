from rest_framework import generics
from boards_app.models import Board
from .serializers import BoardSerializer, BoardDetailSerializer, BoardPatchResponseSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrMember, IsOwner
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from rest_framework.response import Response

class BoardsList(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrMember]

    def perform_create(self, serializer):
        owner_id = self.request.user
        serializer.save(owner=owner_id)
    
    def get_queryset(self):
        user = self.request.user
        qs = Board.objects.filter(Q(members = user) |Q(owner_id=user)).distinct()
        return qs
    

class SingleBoardDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BoardDetailSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrMember]
    queryset = Board.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return BoardPatchResponseSerializer
        return super().get_serializer_class()
    
    
    def get_permissions(self):
        if self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrMember]
        return [permission() for permission in permission_classes]

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
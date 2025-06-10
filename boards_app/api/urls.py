from django.urls import path
from .views import BoardsList, SingleBoardDetail, EmailCheck

urlpatterns = [
    path("boards/", BoardsList.as_view(), name='board-detail'),
    path("boards/<int:pk>/", SingleBoardDetail.as_view(), name="single-detail"),
    path("email-check/<str:email>/", EmailCheck.as_view(), name="email-detail" )
]
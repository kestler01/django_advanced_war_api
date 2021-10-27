from django.urls import path
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.game_views import GamesView, GameDetailView
from .views.piece_views import PiecesView

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),
    path('games/', GamesView.as_view(), name='view-games'),
    path('games/<int:pk>/',GameDetailView.as_view(), name='game-view'),
    path('games/<int:pk>/pieces/', PiecesView.as_view(), name='pieces-view'),
]

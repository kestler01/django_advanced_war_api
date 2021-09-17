from django.urls import path
from .views.mango_views import Mangos, MangoDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.game_views import GamesView, GameDetailView, NewGameView, PiecesView

urlpatterns = [
  	# Restful routing
    path('mangos/', Mangos.as_view(), name='mangos'),
    path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),
    path('games/', GamesView.as_view(), name='view-games'),
    path('games/<int:pk>/',GameDetailView.as_view(), name='game-view'),
    #piece path demos
    path('games/<int:pk>/pieces/', PiecesView.as_view(), name='pieces-view'),
    # other demo path for using new nested writtable relationship serializer
    path('newgame/', NewGameView.as_view(), name='new-game')
    # this is a demo address for testing, and seeing how the relationships are returned in the json responses
    # path('users/<int:pk>', UserDetailView.as_view(), name='user-details') also removed from above
]

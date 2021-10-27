from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.game import Game
from ..serializers import GameSerializer, PieceSerializer, GameDetailsSerializer, ShowPieceSerializer
from ..models.gamePiece import GamePiece

class GamesView(generics.ListCreateAPIView):  # pylint: disable=too-few-public-methods
    """ views associated with many games | use GameSerializer """
    permission_classes = (IsAuthenticated,)

    # get all users games, will have to be edited in V2
    def get(self, request):
        """Index request"""
        games = Game.objects.filter(owner=request.user)
        data = GameSerializer(games, many=True).data
        return Response({'games': data})


    # post to create a game
    def post(self, request):
        """Create request"""
        print("PRINTS in create request view:",request.data)
        request.data['game']['owner'] = request.user.id
        print("PRINTS in create request view AFTER REASSIGNING owner:", request.data)
        game = GameSerializer(data=request.data['game'])
        if game.is_valid():
            game.save()
            return Response({ 'game': game.data }, status=status.HTTP_201_CREATED)
        return Response(game.errors, status=status.HTTP_400_BAD_REQUEST)


class GameDetailView(generics.RetrieveUpdateDestroyAPIView):  # pylint: disable=too-few-public-methods
    """ views associated with one game """
    permission_classes = (IsAuthenticated,)
    # get the one game
    def get(self, request, pk):
        """Show request"""
        game = get_object_or_404(Game, pk=pk)
        # this logic will have to be changed to support more than 1 player in V2
        if request.user != game.owner:
            raise PermissionDenied('Unauthorized, you do not own this game instance')
        data = GameDetailsSerializer(game).data
        return Response({'game': data})

    # delete the game
    def delete(self, request, pk):
        """Delete request"""
        game = get_object_or_404(Game, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != game.owner:
            raise PermissionDenied('Unauthorized, you do not own this game instance')
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk): # V1, update the is_started and is_over fields request is coming in with key gameData, not game as expected
        """Update Request"""
        game = get_object_or_404(Game, pk=pk)
        print("In partial update, the request looks like:", request)
        print("In partial update, the request data looks like:", request.data)
        print("In partial update, this is the target data this function wants to use", request.data['gameData'])
        if request.user != game.owner:
            raise PermissionDenied('Unauthorized, you do not own this game instance')
        request.data['gameData']['owner'] = request.user.id # setting the user.id after checking that it matches si safer than removing the data for now, if it was an empty string for example, it Would rewrite the owner field
        data = GameSerializer(game, data=request.data['gameData'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

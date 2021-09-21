from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.game import Game
from ..serializers import GameSerializer, PieceSerializer, ShowPieceSerializer, ShowGameSerializer
from ..models.game_piece import GamePiece
  #  'id': self.id,
  #  'name': self.name,
  #  'is_started': self.is_started,
  #  'is_over': self.is_over,
  #  'owner': self.owner

class GamesView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
  # start doing my verbs
    # get all users games, will have to be edited in V2
    def get(self, request):
        """Index request"""
        games = Game.objects.filter(owner=request.user)
        data = GameSerializer(games, many=True).data
        return Response({'game': data})

    # post to create a game
    def post(self, request):
        """Create request"""
        print("in post @ game_views", request.data, request.user.id)
        request.data['game']['owner'] = request.user.id
        print(" PRINT AFTER INPOST: LOOKING FOR GAME.OWNER", request.data['game'])
        game = GameSerializer(data=request.data['game'])
        if game.is_valid():
            game.save()
            return Response({ 'game': game.data }, status=status.HTTP_201_CREATED)
        return Response(game.errors, status=status.HTTP_400_BAD_REQUEST)


class GameDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    # get the one game
    def get(self, request, pk):
        """Show request"""
        game = get_object_or_404(Game, pk=pk)
        # this logic will have to be changed to support more than 1 player in V2
        if request.user != game.owner:
            raise PermissionDenied('Unauthorized, you do not own this game instance')
        data = ShowGameSerializer(game).data
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

    def partial_update(self, request, pk): # V1, update the is_started and is_over fields
        """Update Request"""
        game = get_object_or_404(Game, pk=pk)
        if request.user != game.owner:
            raise PermissionDenied('Unauthorized, you do not own this game instance')
        request.data['game']['owner'] = request.user.id # setting the user.id after checking that it matches si safer than removing the data for now, if it was an empty string for example, it Would rewrite the owner field
        data = GameSerializer(game, data=request.data['game'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

# then reintroduce pieces


class PiecesView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        """Index request"""
        # get the piece objects, and filter so we get the ones that belong to this game
        pieces = GamePiece.objects.filter(game=pk)
        data = PieceSerializer(pieces, many=True).data
        return Response({'game_pieces': data})

    # post to create a piece
    def post(self, request, pk):
        """Create request"""
        request.data['piece']['owner'] = request.user.id
        request.data['piece']['game'] = pk
        print(request.data)
        # do i have to do a Game.objects.get(id=pk) to establish this relationship ?
        piece = PieceSerializer(data=request.data['piece'])
        if piece.is_valid():
            piece.save()
            print(piece.data)
            return Response({'piece': piece.data}, status=status.HTTP_201_CREATED)
        return Response(piece.errors, status=status.HTTP_400_BAD_REQUEST)


class PieceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    # get the one piece

    def get(self, request, id, *args, **kwargs):
        """Show request"""
        piece = get_object_or_404(GamePiece, pk=id)
        # this logic will have to be changed to support more than 1 player in V2
        if request.user != piece.owner:
            raise PermissionDenied(
                'Unauthorized, you do not own this piece instance')
        data = ShowPieceSerializer(piece).data
        return Response({'piece': data})

    # delete the piece
    def delete(self, request, id, *args, **kwargs):
        """Delete request"""
        piece = get_object_or_404(GamePiece, pk=id)
        # this logic will have to be changed to support more than 1 player in V2
        if request.user != piece.owner:
            raise PermissionDenied(
                'Unauthorized, you do not own this piece instance')
        piece.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # V1, update position_x and y fields
    def partial_update(self, request, id, *args, **kwargs):
        """Update Request"""
        piece = get_object_or_404(GamePiece, pk=id)
        # this logic will have to be changed to support more than 1 player in V2
        if request.user != piece.owner:  # maybe .player
            raise PermissionDenied(
                'Unauthorized, you do not own this pieceinstance')
        request.data['piece']['owner'] = request.user.id
        data = ShowPieceSerializer(
            piece, data=request.data['piece'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    # currently does NOT update the game pieces if you change them in this request

# AS NESTED RELATIONSHIPS ?!
# class NewGameView(generics.ListCreateAPIView):
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         """Index request"""
#         mangos = Game.objects.filter(owner=request.user)
#         data = GameSerializer(mangos, many=True).data
#         return Response({'game': data})

#     def post(self, request):
#         """Create request"""
#         request.data['game']['owner'] = request.user.id
#         game = NewGameSerializer(data=request.data['game'])
#         if game.is_valid():
#             game.save()
#             return Response({ 'game': game.data }, status=status.HTTP_201_CREATED)
#         return Response(game.errors, status=status.HTTP_400_BAD_REQUEST)
    # then add list of pieces to the game model.
    # patch the game to add and remove pieces.
      # i believe puttin gth object literals in the list is ok* look into this
    # add method to the piece to reassign it's coordinates/move
    # fire off method on a patch request
    # do pieces have owner ?
  #success move to client and begin implementing state and componenets

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..serializers import PieceSerializer, ShowPieceSerializer
from ..models.gamePiece import GamePiece


class PiecesView(generics.ListCreateAPIView):
    """ views for many pieces | use PieceSerializer"""
    permission_classes = (IsAuthenticated,)

    # get this games pieces
    def get(self, request, pk):
        """Index request"""
        # get the piece objects, and filter so we get the ones that belong to this game
        pieces = GamePiece.objects.filter(game=pk)
        data = PieceSerializer(pieces, many=True).data
        return Response({'gamepieces': data})

    # post to create a piece
    def post(self, request, pk):
        """Create request"""
        request.data['piece']['owner'] = request.user.id # sets owner to user that sent request
        request.data['piece']['game'] = pk # sets game to the game instance
        print(request.data)
        piece = PieceSerializer(data=request.data['piece'])
        if piece.is_valid():
            piece.save()
            print(piece.data)
            return Response({'piece': piece.data}, status=status.HTTP_201_CREATED)
        return Response(piece.errors, status=status.HTTP_400_BAD_REQUEST)


class PieceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ views for single pieces"""
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

        if request.user != piece.owner:
        # V3 may not have to change this line if 'player' can be the 'owner' of a piece
            raise PermissionDenied(
                'Unauthorized, you do not own this pieceinstance')
        request.data['piece']['owner'] = request.user.id
        data = ShowPieceSerializer(
            piece, data=request.data['piece'], partial=True)

        if data.is_valid():
            # Save & send a 204 no content / client will have to update local data
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.mango import Mango
from ..serializers import MangoSerializer

# Create your views here.
class Mangos(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = MangoSerializer
    def get(self, request):
        """Index request"""
        # Get all the mangos:
        # mangos = Mango.objects.all()
        # Filter the mangos by owner, so you can only see your owned mangos
        mangos = Mango.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = MangoSerializer(mangos, many=True).data
        return Response({ 'mangos': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['mango']['owner'] = request.user.id
        # Serialize/create mango
        mango = MangoSerializer(data=request.data['mango'])
        # If the mango data is valid according to our serializer...
        if mango.is_valid():
            # Save the created mango & send a response
            mango.save()
            return Response({ 'mango': mango.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(mango.errors, status=status.HTTP_400_BAD_REQUEST)

class MangoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the mango to show
        mango = get_object_or_404(Mango, pk=pk)
        # Only want to show owned mangos?
        if request.user != mango.owner:
            raise PermissionDenied('Unauthorized, you do not own this mango')

        # Run the data through the serializer so it's formatted
        data = MangoSerializer(mango).data
        return Response({ 'mango': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate mango to delete
        mango = get_object_or_404(Mango, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != mango.owner:
            raise PermissionDenied('Unauthorized, you do not own this mango')
        # Only delete if the user owns the  mango
        mango.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Mango
        # get_object_or_404 returns a object representation of our Mango
        mango = get_object_or_404(Mango, pk=pk)
        # Check the mango's owner against the user making this request
        if request.user != mango.owner:
            raise PermissionDenied('Unauthorized, you do not own this mango')

        # Ensure the owner field is set to the current user's ID
        request.data['mango']['owner'] = request.user.id
        # Validate updates with serializer
        data = MangoSerializer(mango, data=request.data['mango'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models.mango import Mango
from .models.user import User
from .models.game import Game
from .models.game_piece import Game_Piece

class MangoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mango
        fields = ('id', 'name', 'color', 'ripe', 'owner')

# wondering if the order here matters, i do have them pointing at each other ...
class PieceSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField()
    # game = serializers.StringRelatedFields() # will return string representation
    # likely unnecessary as the game serializer will print this piece instance too

    class Meta:
        model = Game_Piece
        # id name, game, position_x & y
        fields = ('id', 'name', 'game', 'position_x', 'position_y', 'owner')


class ShowPieceSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    # game = serializers.StringRelatedField()  # will return string representation

    # likely unnecessary as the game serializer will print this too

    class Meta:
        model = Game_Piece
        # id name, game, position_x & y
        fields = ('id', 'name', 'game', 'position_x', 'position_y', 'owner', )

class GameSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField() breaks create game!!!!!!!!
    class Meta:
        model = Game
        fields = ('id', 'name', 'is_over', 'is_started', 'owner', 'turn', 'updated_at', 'created_at') # 'pieces taken out

class GameDetailsSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    game_pieces = PieceSerializer(many=True)
    class Meta:
        model = Game
        fields = ('id', 'name', 'is_over', 'is_started',
                  'owner', 'turn', 'updated_at', 'created_at', 'game_pieces')

# no tin active use this serializer and it's view are experiments that MAY allow for a multifunction route/ combining the pieces and game routes
class NewGameSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    pieces = PieceSerializer(many=True)

    class Meta:
        model = Game
        # id name, is_over, is_started, owner,
        fields = ('id', 'name', 'is_over', 'is_started', 'owner',
                  'turn', 'updated_at', 'created_at', 'pieces')
    # this is a writable custom method so we can set up the game with pieces on create
    # assuming it is set up correctly

    def create(self, validated_data):
      pieces_data = validated_data.pop('pieces')
      game = Game.objects.create(**validated_data)
      for piece_data in pieces_data:  # requests will have to use piece_data
          Game_Piece.objects.create(game=game, owner=game.owner, **piece_data)
      return game


# /////////////////////////////////////////////////////////////////////////////////////////
# From https://www.django-rest-framework.org/api-guide/relations/
# Writtable nested relationships example
# By default nested serializers are read-only. If you want to support write-operations to a
# nested serializer field you'll need to create create() and/or update() methods in order
# to explicitly specify how the child relationships should be saved:
#   class TrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Track
#         fields = ['order', 'title', 'duration']

# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = TrackSerializer(many=True)

#     class Meta:
#         model = Album
#         fields = ['album_name', 'artist', 'tracks']

#     def create(self, validated_data):
#         tracks_data = validated_data.pop('tracks')
#         album = Album.objects.create(**validated_data)
#         for track_data in tracks_data:
#             Track.objects.create(album=album, **track_data)
#         return album


# >> > data = {
#     'album_name': 'The Grey Album',
#     'artist': 'Danger Mouse',
#     'tracks': [
#         {'order': 1, 'title': 'Public Service Announcement', 'duration': 245},
#         {'order': 2, 'title': 'What More Can I Say', 'duration': 264},
#         {'order': 3, 'title': 'Encore', 'duration': 159},
#     ],
# }
# >> > serializer = AlbumSerializer(data=data)
# >> > serializer.is_valid()
# True
# >> > serializer.save()
# ////////////////////////////////////////////////////////////////////////////////////////

class UserSerializer(serializers.ModelSerializer):
    # This model serializer will be used for User creation
    # The login serializer also inherits from this serializer
    # in order to require certain data for login
    class Meta:
        # get_user_model will get the user model (this is required)
        # https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = { 'password': { 'write_only': True, 'min_length': 5 } }

    # This create method will be used for model creation
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

class UserRegisterSerializer(serializers.Serializer):
    # Require email, password, and password_confirmation for sign up
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError('Please include a password and password confirmation.')

        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Please make sure your passwords match.')
        # if all is well, return the data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)

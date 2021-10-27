from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models.mango import Mango
from .models.game import Game
from .models.gamePiece import GamePiece


class MangoSerializer(serializers.ModelSerializer):  # pylint: disable=too-few-public-methods
    """ from template should be deleted, afraid to break migrations """
    class Meta:  # pylint: disable=too-few-public-methods
        """ ignore me """
        model = Mango
        fields = ('id', 'name', 'color', 'ripe', 'owner')

# wondering if the order here matters, i do have them pointing at each other ...

class PieceSerializer(serializers.ModelSerializer):  # pylint: disable=too-few-public-methods
    """ serializer for game_pieces,
    DO NOT PUT related fields in here: there are redundant,
     used when creating pieces """
    class Meta:  # pylint: disable=too-few-public-methods
        """ V1: id name, game, position_x & y
        V2: ...V1, + movement_points, can_cap, hit_points, attack_range, base_attack, base_defense,
          unit_type
        all V2 fields have defaults """
        model = GamePiece
        fields = ('id', 'name', 'game', 'position_x',
                  'position_y', 'owner', 'movement_points', 'can_cap', 'hit_points', 'attack_range',
                  'base_attack', 'base_defense', 'unit_type')


class ShowPieceSerializer(serializers.ModelSerializer):  # pylint: disable=too-few-public-methods
    """ serializer for game_pieces after they are created, can use related fields:
    game points at pieces already so that one is redundant - do not loop it"""
    owner = serializers.StringRelatedField()

    class Meta:  # pylint: disable=too-few-public-methods
        """ same as the pieceSerializer but has the field reference for owner """
        model = GamePiece
        fields = ('id', 'name', 'game', 'position_x',
                  'position_y', 'owner', 'movement_points', 'can_cap', 'hit_points', 'attack_range',
                  'base_attack', 'base_defense', 'unit_type')


class GameSerializer(serializers.ModelSerializer):  # pylint: disable=too-few-public-methods
    """ used for creating games
    owner = serializers.StringRelatedField() breaks create game = bad day"""
    class Meta:  # pylint: disable=too-few-public-methods
        """ V1, V2 to include a 'players' field which will include the owner
        also a 2nd signed in user who will be able to move their pieces
        to be added in gameversion 3 when integrating sockets """
        model = Game
        fields = ('id', 'name', 'is_over', 'is_started', 'owner', 'turn', 'updated_at',
                  'created_at', 'size')
        # currently game pieces are not created at game creation
        # this is good for V3 when a game is made but not started / P2 is unknown


class GameDetailsSerializer(serializers.ModelSerializer):  # pylint: disable=too-few-public-methods
    """ serializer for singular games after they are created, can use related fields """
    owner = serializers.StringRelatedField()
    game_pieces = PieceSerializer(many=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """ V1.5 adds size | V2+ add players to be done with sockets integration"""
        model = Game
        fields = ('id', 'name', 'is_over', 'is_started',
                  'owner', 'turn', 'updated_at', 'created_at', 'game_pieces', 'size')

    def create(self, validated_data):
        """ method to create pieces when they are listed in the game_pieces array
        unsure if necessary or if it's implemented? """
        pieces_data = validated_data.pop('pieces')
        game = Game.objects.create(**validated_data)
        for piece_data in pieces_data:  # requests will have to use piece_data
            GamePiece.objects.create(game=game, owner=game.owner, **piece_data)
        return game

class UserSerializer(serializers.ModelSerializer):
    """ This model serializer will be used for User creation
    The login serializer also inherits from this serializer
    in order to require certain data for login """
    class Meta:
        """ get_user_model will get the user model (this is required)
        https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#referencing-the-user-model"""
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = { 'password': { 'write_only': True, 'min_length': 5 } }

    def create(self, validated_data):
        """ This create method will be used for model creation """
        return get_user_model().objects.create_user(**validated_data)

class UserRegisterSerializer(serializers.Serializer):
    """ Require email, password, and password_confirmation for sign up """
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        """ validates the passwords to make sure they match and exist """
        # Ensure password & password_confirmation exist
        if not data['password'] or not data['password_confirmation']:
            raise serializers.ValidationError('Please include a password and password confirmation.')

        # Ensure password & password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Please make sure your passwords match.')
        # if all is well, return the data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    """ Used for changing passwords anf requires both a new and the old password """
    model = get_user_model()
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)

from django.db import models
from django.contrib.auth import get_user_model
from .game import Game


class GamePiece(models.Model):  # pylint: disable=too-few-public-methods
    """ default test class for movable Game Pieces"""
    name = models.CharField(
      default="test",
      max_length=100
    )
    owner = models.ForeignKey(
        get_user_model(),
        related_name='game_pieces',
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        Game,
        related_name= 'game_pieces',
        on_delete=models.CASCADE
    )
    # correspond to game grid cells. currently playing on 7 by 7 board
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    # start of V2 fields!
    # how far can a piece move, some square will require more points
    movement_points = models.IntegerField(default=2)
    # can this piece capture income points?
    can_cap = models.BooleanField(default=True)
    # how much damage has the unit taken
    hit_points = models.IntegerField(default=100)
    # how far away it can attack from
    attack_range = models.IntegerField(default=1)
    # base damage to dealt when at full health
    base_attack = models.IntegerField(default=60)
    # base damage mitigation if any
    base_defense = models.IntegerField(default=0)
    # unit type - potentially to be used with a vs type chart for multipliers ?
    # should use choices and set max length reasonably,
    # current value of 100 is unnecessarily large
    # alternative is to have this default class be inherited by the other pieces
    # have them have hard defined values
    unit_type = models.CharField(
      default="test",
      max_length=100
    )
    # need to add a hasActed / moved variable to make sure you can't multi move a piece indefinitely before V3

from django.db import models
from django.contrib.auth import get_user_model
# from django.db.models.fields import IntegerField
from .game import Game
# Create your models here.
# Vague starter piece to build the others off of. Also proof of concept.
class Game_Piece(models.Model):
    # define fields
    # https://docs.djangoproject.com/en/3.0/ref/models/fields/
    name = models.CharField(max_length=100)
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
    # movement points ? ( or should this class just be a parent class to write all the other ones from )

    def move(self, new_x, new_y):  # new_x/y are ints
        # method to reassign position, logic checks to be done elsewhere
        self.position_x = new_x
        self.position_y = new_y
        # don't forget to save the changes!
        self.save()
        return (self.position_x, self.position_y)

    def __str__(self):
        """Return string representation of the piece"""
        return ( f" {self.owner}s {self.name} piece, in {self.game}game, is at ({self.position_x},{self.position_y}")

    def __dict__(self):
        return {
            'id':self.id,
            'game': self.game,
            'name' : self.name,
            'owner' : self.owner,
            'position_x' : self.position_x,
            'position_y' : self.position_y,
        }
# class Marine(Game_piece):
#     name= 'marine'

# class Soldier(Game_piece):
    # # 'how far can I move?', but using this variable because not all moves are equal in later versions
    # base_action_points = models.IntegerField(default=3)
    # action_points = models.IntegerField(default=base_action_points)
    # # the 'health' of the unit'
    # base_hit_points = models.IntegerField(default=100)
    # hit_points = models.IntegerField(default=base_hit_points)
    # # how much hit_points will be deducted form another piece
    # base_attack = models.IntegerField(default=50)
    # attack = models.IntegerField(default=base_attack)
    # # an int to be implemented as a ratio to scale attack effect on hit points ex: thisAttack=attack/defense
    # defense = models.IntegerField(default=1)
    # unit_type = models.CharField(max_length=100) # infantry,spear,archer,calvary, implement as choices ?

    # def take_damage(self, damage): # damage = int
    #     #this method accepts damage to reduce hit points by, after reducing through the defense ratio(default 1)
    #     dmg = damage / self.defense
    #     self.hit_points -= dmg
    #     if self.hit_points<=0:
    #         self.delete()
    #         print("your piece has lost all it's hit points and has been removed")

    # def attack(self, target_id): # needs a target, will return an int and trigger the take_damage on that piece
        # get the target soldier by it's id
        # run targets take_damage, and pass it self.attack as the damage arg

    # def __dict__(self):
    #   return {
    #     'id': self.id,
    #     'game' : self.game,
    #     'name' : self.name,
    #     'owner' : self.owner,
    #     'position_x' : self.position_x,
    #     'position_y' : self.position_y,
    #     'base_action_points' : self.base_action_points,
    #     'action_points' : self.action_points,
    #     'base_hit_points': self.base_hit_points,
    #     'hit_points' : self.hit_points,
    #     'base_attack' : self.base_attack,
    #     'attack' : self.attack,
    #     'defense' : self.defense,
    #     'unit_type' : self.unit_type
    #   }

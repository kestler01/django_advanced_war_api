from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.postgres.fields import ArrayField

class Game(models.Model):
    """ class for game instances| to create requires a name """
    name = models.CharField(max_length=100)
    is_over = models.BooleanField(default= False)
    is_started = models.BooleanField(default=False)
    owner = models.ForeignKey(
        get_user_model(),
        related_name= 'games',
        on_delete=models.CASCADE
    )
    turn = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # V2 fields
    size = models.IntegerField(default=7)

    def __str__(self):
        return f"This game instance is named{self.name}, id:{self.id} and is owned by{self.owner}"

    def as_dict(self):
        """Returns dictionary version of Mango models"""
        return {
            'id': self.id,
            'name': self.name,
            'is_started':self.is_started,
            'is_over': self.is_over,
            'owner': self.owner,
            'turn': self.turn,
            'created_at' : self.created_at,
            'updated_at' : self.updated_at
            # 'players': self.players
        }

    # V2+
    # participating players
    # players = models.ForeignKey(
    #     # will reference a user
    #     get_user_model(),
    #     #not sure if necessary, but adding this field doesn't hurt
    #     related_name='joined_game',
    #     # if a user is deleted from the database we don't delete the game
    #     on_delete=models.SET_NULL,
    #     #can be empty
    #     blank=True,
    #     #can have a null value
    #     null=True,
    #     # #can have several players ( 2 )
    #     # many=True
    # )

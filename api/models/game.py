from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.postgres.fields import ArrayField

class Game(models.Model):
  # define fields
  # https://docs.djangoproject.com/en/3.0/ref/models/fields/

  # nameable is good for searching list to pair game
  name = models.CharField(max_length=100)
  # bool to reassign if game is over, may be useful if it is decided that games should be stored and retrieved
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

  def __str__(self):
    # This must return a string
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

    # could i make a one to many game to cells relationship ?

  # V2
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

  # the money!, should be a table with key value pairs corresponding to piece postitions ?
    # how to get JS to play nice with a table, iterate through it like its an array? make it an array of arrays ?
  # psql array of arrays. the arrays are indexed representing the coordinates, and the values are the pieces or empty, (and later coordinate location info, V3 )
  # class ArrayField(base_field, size=None, **options)
    #base_field This is a required argument.
    # Specifies the underlying data type and behavior for the array. It should be an instance of a subclass of Field. For example, it could be an IntegerField or a CharField.

    # It is possible to nest array fields - you can specify an instance of ArrayField as the base_field

    # !!!!!! Most field types are permitted, with the exception of those handling relational data (ForeignKey, OneToOneField and ManyToManyField)!!!!!!

    # SO: I have to rethink how to model this data..., do i just have the pieces have a location on it that represents that space WITHOUT the relationship, as long as the relationship to the game object here is maintained it should be fine ... ?
    # if thats the case do i even NEED a board attribute ?

    # board = ArrayField( #odd sizes will allow symmetry through a center piece
    #         ArrayField(
    #           'base_field',
    #           size=7,
    #           #'options'
    #         ),
    #     size=7
    #     )

    # if i can't put them in board, i will make them reference this game and have position ?

    # i could set up a hard coded grid.

    # I will send EVERYTHING over to the client with the serializer and sort it out there

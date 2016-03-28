from google.appengine.ext import ndb
from protorpc import messages

INITIAL_BOARD = [ '  ***  ',
                  '  ***  ',
                  '*******',
                  '***o***',
                  '*******',
                  '  ***  ',
                  '  ***  '
                ]

class User(ndb.Model):
    """ User profile """
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)

class GameMessage(messages.Message):
    """ Transferable Game State Information """
    user = messages.StringField(1)
    board = messages.StringField(2, repeated=True)
    game_over = messages.BooleanField(3)
    urlsafe_key = messages.StringField(4)

class GameKeyMessage(messages.Message):
    game_key = messages.StringField(1, required=True)

class Game(ndb.Model):
    """ Game Object """
    user = ndb.KeyProperty(required=True)
    board = ndb.PickleProperty(required=True)
    game_over = ndb.BooleanProperty(required=True, default=False)

    @classmethod
    def new_game(cls, user):
        game=cls(user=user, board=INITIAL_BOARD)
        game.put()
        return game

    def to_message(self):
        return GameMessage(user=self.user.get().name,
                           board=self.board,
                           game_over=self.game_over,
                           urlsafe_key=self.key.urlsafe)

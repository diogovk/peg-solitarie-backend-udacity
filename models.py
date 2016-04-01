from google.appengine.ext import ndb
from rpc_messages import GameMessage, GamesMessage, GameKeyMessage
from gamelogic import INITIAL_BOARD


class User(ndb.Model):
    """ User profile """
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    high_score = ndb.IntegerProperty(default=0)


class Game(ndb.Model):
    """ Game Object """
    user = ndb.KeyProperty(required=True)
    board = ndb.PickleProperty(required=True)
    game_over = ndb.BooleanProperty(required=True, default=False)
    history = ndb.StringProperty(repeated=True)
    score = ndb.IntegerProperty()

    @classmethod
    def new_game(cls, user):
        game = cls(user=user, board=INITIAL_BOARD, history=[])
        game.put()
        return game

    def to_message(self):
        return GameMessage(user=self.user.get().name,
                           board=self.board,
                           game_over=self.game_over,
                           urlsafe_key=self.key.urlsafe(),
                           history=self.history,
                           score=self.score)

    @classmethod
    def get_from_key(cls, urlsafe_key):
        game_key = ndb.Key(urlsafe=urlsafe_key)
        game = game_key.get()
        if game_key.kind() != cls.__name__:
            raise ValueError('Incorrect Kind')
        return game

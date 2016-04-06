from google.appengine.ext import ndb
from rpc_messages import GameMessage, GamesMessage, GameKeyMessage
from rpc_messages import ScoreMessage, UserHighScore, GameHistoryMessage
from gamelogic import INITIAL_BOARD


class User(ndb.Model):
    """ User profile """
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    high_score = ndb.IntegerProperty(default=0)

    def to_highscoremessage(self):
        return UserHighScore(username=self.name, high_score=self.high_score)

    def update_high_score(self, game):
        """
        Checks if game's score is higher than the user's high score.
        If it is, sets the user high_score to game's score
        """
        if game.score > self.high_score:
            self.high_score = game.score


class Game(ndb.Model):
    """ Game Object """
    user = ndb.KeyProperty(required=True)
    board = ndb.PickleProperty(required=True)
    game_over = ndb.BooleanProperty(required=True, default=False)
    history = ndb.StringProperty(repeated=True)
    score = ndb.IntegerProperty()
    ended_at = ndb.DateProperty()

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

    def to_scoremessage(self):
        return ScoreMessage(username=self.user.get().name,
                            score=self.score,
                            date=str(self.ended_at))

    def to_historymessage(self):
        return GameHistoryMessage(history=self.history)

    @classmethod
    def get_from_key(cls, urlsafe_key):
        game_key = ndb.Key(urlsafe=urlsafe_key)
        game = game_key.get()
        if game_key.kind() != cls.__name__:
            raise ValueError('Incorrect Kind')
        return game

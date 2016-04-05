import endpoints
from protorpc import messages

RC_GAME_KEY = endpoints.ResourceContainer(
        game_key=messages.StringField(1))


class NumberOfResultsMessage(messages.Message):
    """ In a consult, tell how many entries to fetch """
    number_of_results = messages.IntegerField(1)


class UserHighScore(messages.Message):
    """ A ranking entry, which is a user and it's highest score """
    username = messages.StringField(1, required=True)
    high_score = messages.IntegerField(2, required=True)


class RankingMessage(messages.Message):
    """ A Ranking of users with the highest scores """
    ranking = messages.MessageField(UserHighScore, 1, repeated=True)


class ScoreMessage(messages.Message):
    """ Message representing a game result """
    username = messages.StringField(1, required=True)
    score = messages.IntegerField(2, required=True)
    date = messages.StringField(3, required=True)


class LeaderboardMessage(messages.Message):
    """ A group of Score Messages representing a Leaderboard """
    leaderboard = messages.MessageField(ScoreMessage, 1, repeated=True)


class MoveMessage(messages.Message):
    """ Form used to make a Move request in a game. """
    origin_point = messages.StringField(1)
    direction = messages.StringField(2)


RC_MAKE_MOVE = endpoints.ResourceContainer(
        MoveMessage,
        game_key=messages.StringField(1))


class GameMessage(messages.Message):
    """ Transferable Game State Information """
    user = messages.StringField(1)
    board = messages.StringField(2, repeated=True)
    game_over = messages.BooleanField(3)
    urlsafe_key = messages.StringField(4)
    history = messages.StringField(5, repeated=True)
    score = messages.IntegerField(6)


class GamesMessage(messages.Message):
    games = messages.MessageField(GameMessage, 1, repeated=True)


class GameKeyMessage(messages.Message):
    game_key = messages.StringField(1, required=True)


class StringMessage(messages.Message):
    message = messages.StringField(1, required=True)


class UserMessage(messages.Message):
    user = messages.StringField(1, required=True)


class NewUserMessage(messages.Message):
    username = messages.StringField(1, required=True)
    email = messages.StringField(2, required=True)

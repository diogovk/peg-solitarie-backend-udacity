import endpoints
from protorpc import messages

RC_GAME_KEY = endpoints.ResourceContainer(
        game_key=messages.StringField(1))


class GameMessage(messages.Message):
    """ Transferable Game State Information """
    user = messages.StringField(1)
    board = messages.StringField(2, repeated=True)
    game_over = messages.BooleanField(3)
    urlsafe_key = messages.StringField(4)


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
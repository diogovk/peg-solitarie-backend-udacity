import endpoints
from protorpc import remote
from protorpc import messages
from protorpc import message_types
from models import User

class StringMessage(messages.Message):
    message = messages.StringField(1, required=True)

class BoardMessage(messages.Message):
    board = messages.StringField(1, repeated=True)

INITIAL_BOARD = BoardMessage(board=[
               '  ***  ',
               '  ***  ',
               '*******',
               '***o***',
               '*******',
               '  ***  ',
               '  ***  '
               ])

class UserMessage(messages.Message):
    user = messages.StringField(1, required=True)

class NewUserMessage(messages.Message):
    username = messages.StringField(1, required=True)
    email = messages.StringField(2, required=True)

@endpoints.api(name='peg_solitarie', version='v1')
class PegSolitarieAPI(remote.Service):
    " Peg Solitararie Game API"

    @endpoints.method(request_message=UserMessage,
                      response_message=BoardMessage,
                      path="new_game",
                      name="new_game",
                      http_method='GET')
    def new_game(self, request):
        return INITIAL_BOARD

    @endpoints.method(request_message=NewUserMessage,
                      response_message=StringMessage,
                      path="user",
                      name="new_user",
                      http_method="POST")
    def new_user(self, request):
        return StringMessage(message="dood")



api = endpoints.api_server([PegSolitarieAPI])



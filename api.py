import endpoints
from protorpc import remote
from protorpc import messages
from protorpc import message_types



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

api = endpoints.api_server([PegSolitarieAPI])



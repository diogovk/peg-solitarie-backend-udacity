import endpoints
from protorpc import remote
from protorpc import messages
from protorpc import message_types



class StringMessage(messages.Message):
        string = messages.StringField(1)

@endpoints.api(name='peg_solitarie', version='v1')
class PegSolitarieAPI(remote.Service):
    " Peg Solitararie Game API"

    @endpoints.method(request_message=message_types.VoidMessage,
                      response_message=StringMessage,
                      path="hello",
                      name="hello",
                      http_method='GET')
    def hello(self, request):
        return StringMessage(string="superdood")

api = endpoints.api_server([PegSolitarieAPI])



import endpoints
from protorpc import remote
from models import User, Game
from rpc_messages import GameMessage, GamesMessage, GameKeyMessage, RC_GAME_KEY
from rpc_messages import StringMessage, UserMessage, NewUserMessage, MoveMessage
from rpc_messages import RC_MAKE_MOVE
from gamelogic import move, InvalidMoveExpection


@endpoints.api(name='peg_solitarie', version='v1')
class PegSolitarieAPI(remote.Service):
    " Peg Solitararie Game API"

    @endpoints.method(request_message=UserMessage,
                      response_message=GameMessage,
                      path="new_game",
                      name="new_game",
                      http_method='GET')
    def new_game(self, request):
        """ Creates a new game """
        user = User.query(User.name == request.user).get()
        if not user:
            raise endpoints.NotFoundException("This user doesn't exist")
        game = Game.new_game(user=user.key)
        return game.to_message()

    @endpoints.method(request_message=RC_GAME_KEY,
                      response_message=GameMessage,
                      path="game/{game_key}",
                      name="get_game",
                      http_method="GET")
    def get_game(self, request):
        """ Returns the current state of a certain game """
        game = Game.get_from_key(urlsafe_key=request.game_key)
        if game:
            return game.to_message()
        else:
            raise endpoints.NotFoundException("The game could not be found")

    @endpoints.method(request_message=NewUserMessage,
                      response_message=StringMessage,
                      path="user",
                      name="new_user",
                      http_method="POST")
    def new_user(self, request):
        """ Creates a new user. Requires a unique username """
        if User.query(User.name == request.username).get():
            raise endpoints.ConflictException(
                    "A user with this username already exists")
        user = User(name=request.username, email=request.email)
        user.put()
        return StringMessage(message="User successfully created.")

    @endpoints.method(request_message=UserMessage,
                      response_message=GamesMessage,
                      path="user/games",
                      name="get_active_games",
                      http_method="GET")
    def get_active_games(self, request):
        """ Get all active games being played by a player """
        user = User.query(User.name == request.user).get()
        if not user:
            raise endpoints.NotFoundException("This user doesn't exist")
        games = Game.query(Game.user == user.key).filter(
                    Game.game_over == False)
        return GamesMessage(games=[game.to_message() for game in games])

    @endpoints.method(request_message=RC_GAME_KEY,
                      response_message=StringMessage,
                      path="game/{game_key}",
                      name="cancel_game",
                      http_method="DELETE")
    def cancel_game(self, request):
        """ Delete a non-ended game """
        game = Game.get_from_key(urlsafe_key=request.game_key)
        if not game:
            raise endpoints.NotFoundException("The game could not be found")
        if game.game_over:
            raise endpoints.BadRequestException("The game is already over!")
        else:
            game.key.delete()
            return StringMessage(message="Game successfully canceled.")

    @endpoints.method(request_message=RC_MAKE_MOVE,
                      response_message=GameMessage,
                      path="game/{game_key}",
                      name="make_move",
                      http_method="PUT")
    def make_move(self, request):
        game = Game.get_from_key(urlsafe_key=request.game_key)
        if not game:
            raise endpoints.NotFoundException("The game could not be found")
        try:
            response =  move(game.to_message(), (request.origin_point, request.direction))
        except (ValueError, InvalidMoveExpection) as e:
            raise endpoints.BadRequestException(e.message)
        return response

api = endpoints.api_server([PegSolitarieAPI])

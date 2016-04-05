import endpoints
from protorpc import remote
from models import User, Game
from rpc_messages import GameMessage, GamesMessage, GameKeyMessage, MoveMessage
from rpc_messages import StringMessage, UserMessage, NewUserMessage
from rpc_messages import RC_MAKE_MOVE, RC_GAME_KEY, NumberOfResultsMessage
from rpc_messages import LeaderboardMessage
import gamelogic
from google.appengine.ext import ndb


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
                      name="get_user_games",
                      http_method="GET")
    def get_user_games(self, request):
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
        """ Make move in the game, returning the new game """
        game = Game.get_from_key(urlsafe_key=request.game_key)
        if not game:
            raise endpoints.NotFoundException("The game could not be found")
        try:
            game = gamelogic.make_move(
                    game, (request.origin_point, request.direction))
        except (ValueError, gamelogic.InvalidMoveExpection) as e:
            raise endpoints.BadRequestException(e.message)
        if game.game_over:
            gamelogic.end_game(game)
            self.commit_game_end(game)
        else:
            game.put()
        return game.to_message()

    @endpoints.method(request_message=RC_GAME_KEY,
                      response_message=StringMessage,
                      path="give_up/{game_key}",
                      name="give_up",
                      http_method="PUT")
    def give_up(self, request):
        """
        Gives up a game. The game will be ended and scores will be calculated.
        """
        game = Game.get_from_key(urlsafe_key=request.game_key)
        if not game:
            raise endpoints.NotFoundException("The game could not be found")
        if game.game_over:
            raise endpoints.BadRequestException("The game is already over")
        gamelogic.end_game(game)
        self.commit_game_end(game)
        return StringMessage(message="Game ended. Score: %s." % game.score)

    @endpoints.method(request_message=NumberOfResultsMessage,
                      response_message=LeaderboardMessage,
                      path="user",
                      name="get_high_scores",
                      http_method="GET")
    def get_high_scores(self, request):
        """ Gets a Leaderboard. A list of games with the highest recorded scores. """
        games = Game.query().filter(Game.score > 0).order(-Game.score)
        if request.number_of_results:
            games = games.fetch(request.number_of_results)
        return LeaderboardMessage(
                leaderboard=[g.to_scoremessage() for g in games])

    @ndb.transactional(xg=True)
    def commit_game_end(self, game):
        """
        Receives an ended game (including its score) and updates the player's
        top high score if necessary, commiting both in the database.
        """
        user = game.user.get()
        user.update_high_score(game)
        user.put()
        game.put()


api = endpoints.api_server([PegSolitarieAPI])

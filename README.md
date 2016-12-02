# peg-solitarie-backend-udacity
Project 4 of my udacity course

## The Game

The chosen game is Peg Solitarie [Peg Solitarie](https://en.wikipedia.org/wiki/Peg_solitaire).
Peg solitaire is a single-player board game involving movement of pegs on a board with holes.
The standard game fills the entire board with pegs except for the central hole. The objective is, making valid moves, to empty the entire board except for a solitary peg in the central hole.
A valid move is to jump a peg orthogonally over an adjacent peg into a hole two positions away and then to remove the jumped peg.

This is what a peg solitarie board looks like:
```
   a b c d e f g
 1     * * *
 2     * * *
 3 * * * * * * *
 4 * * * o * * *
 5 * * * * * * *
 6     * * *
 7     * * *
```

\* represents a peg, and o represents a hole.

## The Score

Each removed peg gives 1 point. Ending the game with a peg in the center gives 5 points.
The maximum achievable score is 36.


## Dependencies

```
python2
Google App Engine SDK for Python (google-appengine-python)
```

## Getting started

### Start local server
```
dev_appserver.py .
```
After that you'll be able to access your application in http://localhost:8080/_ah/api/peg_solitarie/v1/.

### Exploring the API

After starting the local server, open Chrome/Chromium with the following command line:
```
google-chrome-stable  --user-data-dir=/tmp/mytest --unsafely-treat-insecure-origin-as-secure=http://localhost:8080 http://localhost:8080/_ah/api/explorer
```



### Deploy to Google App engine
```
appcfg.py -A peg-solitarie-backend-udacity -V v1 update .
```
After deploying you can access the application in http://v1.peg-solitarie-backend-udacity.appspot.com/

Change "peg-solitarie-backend-udacity" for your app engine application identification as needed.
If you do, remember to update it in app.yaml as well.


### Run Game Logic tests
```
python2 test_logic.py
```


##Files Included:
 - api.py: Contains endpoints.
 - app.yaml: App configuration.
 - cron.yaml: Cronjob configuration.
 - main.py: Handler for cron jobs.
 - models.py: Entity definitions including helper methods.
 - rpc_messages.py: RPC Messages definitions.
 - gamelogic.py: Game Logic functions.
 - test_logic.py: Tests for game Logic

##Endpoints Included:
 - **create_user**
    - Path: 'user'
    - Method: POST
    - Parameters: username, email (optional)
    - Returns: Message confirming creation of the User.
    - Description: Creates a new User. username provided must be unique. Will
    raise a ConflictException if a User with that username already exists.

 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: user
    - Returns: GameMessage with initial game state.
    - Description: Creates a new Game. user must correspond to the username of
    an existing User - will raise a NotFoundException if not.

 - **get_game**
    - Path: 'game/{game_key}'
    - Method: GET
    - Parameters: game_key
    - Returns: GameMessage with current game state.
    - Description: Returns the current state of a game. Will raise
    NotFoundException if game doesn't exist.

 - **make_move**
    - Path: 'game/{game_key}'
    - Method: PUT
    - Parameters: game_key, origin_point, direction
    - Returns: GameMessage with new game state.
    - Description: Move a peg in the board, if the movement is valid. game_key
    is the key of the game where the move should be made. origin_point is the
    position of the peg which will "jump" another peg. direction is the
    direction of the movement and can be 'up', 'down', 'left', 'right'. The
    game will be ended if there's only one peg left in the board.

  - **get_user_games**
     - Path: 'user/games'
     - Method: GET
     - Parameters: user
     - Returns: GameMessages with the state of the active games.
     - Description: Get all active games being played by the User with that
     username.

  - **cancel_game**
     - Path: 'game/{game_key}'
     - Method: DELETE
     - Parameters: game_key
     - Returns: Message confirming game deletion
     - Description: Delete a non-ended game.  Will raise NotFoundException if
     a game with game_key doesn't exist and raise BadRequestException if the
     requested game is already over.

- **give_up**
   - Path: 'give_up/{game_key}'
   - Method: PUT
   - Parameters: game_key
   - Returns: Messsage confirming the game has ended
   - Description: Gives up a game. The game with game_key will be ended and
   scores will be calculated. Will raise NotFoundException if game doesn't
   exist and BadRequestException if game is already over.

- **get_high_scores**
   - Path: 'leaderboard'
   - Method: GET
   - Parameters: number_of_results (optional)
   - Returns: LeaderboardMessage containing the highest score games.
   - Description: Gets a Leaderboard, the list of games with the highest
   recorded scores. If number_of_results is specified, at most number_of_results
   entries will be returned.

- **get_user_rankings**
   - Path: 'user/ranking'
   - Method: GET
   - Parameters: None
   - Returns: RankingMessage
   - Description: A raking listing users with the highest recorded scores.

- **get_game_history**
   - Path: 'game/{game_key}/history'
   - Method: GET
   - Parameters: game_key
   - Returns: GameHistoryMessage
   - Description: Gets the movement history for a specific game.  Each
   moviement is composed of two fields separated by colon.  The first
   is the origin point in the board. The second is the direction which
   can be 'u', 'd', 'l', 'r' for 'up', 'down', 'left' and 'right'
   respectively.

##Models Included:
  - **User**
    - Stores unique username and (optional) email address.

  - **Game**
    - Stores unique game states. Associated with User model via KeyProperty.

##Forms(RPC Messages) included
 - **NumberOfResultsMessage**
    - (Inbound) Maximum number of results in a query (number_of_results)
 - **UserHighScore**
    - (Outbound) Entries in RankingMessage (username, high_score)
 - **RankingMessage**
    - (Outbound) A list of users and their high_scores (ranking)
 - **ScoreMessage**
    - (Outbound) Entries in LeaderboardMessage (username, score, date)
 - **LeaderboardMessage**
    - (Outbound) A list of scores representing a leaderboard (leaderboard)
 - **MoveMessage**
    - (Inbound) A peg movement in the game (origin_point, direction)
 - **GameMessage**
    - (Outbound) Game state (user, board, game_over, urlsafe_key, history,
    score)
 - **GamesMessage**
    - (Outbound) A group of GameMessages (games)
 - **GameKeyMessage**
    - (Inbound) The urlsafe key of a game (game_key)
 - **GameHistoryMessage**
    - (Outbound) Movement history of a game (history)
 - **StringMessage**
    - (Outbound) Simple Messages containing a String (message)
 - **UserMessage**
    - (Inbound) The unique username of a User (user)
 - **NewUserMessage**
    - (Inbound) The register form of a User (username, email)

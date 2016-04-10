# peg-solitarie-backend-udacity
Project 4 of my udacity course

## The Game

The chosen game is Peg Solitarie [Peg Solitarie](https://en.wikipedia.org/wiki/Peg_solitaire).
Peg solitaire is a single-player board game involving movement of pegs on a board with holes. 
The standard game fills the entire board with pegs except for the central hole. The objective is, making valid moves, to empty the entire board except for a solitary peg in the central hole.
A valid move is to jump a peg orthogonally over an adjacent peg into a hole two positions away and then to remove the jumped peg.

This is what a peg solitarie board looks like:
   a b c d e f g
 1     * * *
 2     * * *
 3 * * * * * * *
 4 * * * o * * *
 5 * * * * * * *
 6     * * *
 7     * * *

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
After that you'll be able to access your application in http://localhost:8080/_ah/api/explorer.

### Exploring the API

After starting the local server, open Chrome/Chromium with the following command line:
```
chromium  --user-data-dir=test --unsafely-treat-insecure-origin-as-secure=http://localhost:8080
```
Then access the api explorer with the following URL http://localhost:8080/_ah/api/explorer.



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
    - Description: Creates a new User. user_name provided must be unique. Will
    raise a ConflictException if a User with that user_name already exists.

 - **new_game**
    - Path: 'game'
    - Method: POST
    - Parameters: username
    - Returns: GameMessage with initial game state.
    - Description: Creates a new Game. username provided must correspond to an
    existing user - will raise a NotFoundException if not. 

 - **get_game**
    - Path: 'game/{game_key}'
    - Method: GET
    - Parameters: game_key
    - Returns: GameMessage with current game state.
    - Description: Returns the current state of a game.


 - **make_move**
    - Path: 'game/{game_key}'
    - Method: PUT
    - Parameters: game_key, origin_point, direction
    - Returns: GameMessage with new game state.
    - Description: Accepts a 'guess' and returns the updated state of the game.
    If this causes a game to end, the score of the game will be calculated.

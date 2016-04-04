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
After that you'll be able to access your application in http://localhost:8080/

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


### Run Game Logic tests
```
python2 test_logic.py
```

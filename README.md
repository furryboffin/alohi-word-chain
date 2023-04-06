# Alohi Word Chain Game

This project creates a REST API that exposes the following endpoints:

```
/api/v1.0/game/new (POST)
/api/v1.0/game/end (POST)
/api/v1.0/game/word (POST)
/api/v1.0/game/history (GET)
```

Post data are as follows:

To start a new game POST to /game/new :
```
{
  "email":"email@example.com"
}
```

you will receive a json containing the game_id

To play the game POST to /game/word :
```
{
    "email":"email@example.com",
    "word":"zoom",
    "game_id": GAME_ID
}
```

To end the game POST to /game/end :
```
{
    "email":"email@example.com",
    "game_id": GAME_ID
}
```

To get history of a game GET to /game/history :
```
{
    "email":"email@example.com",
    "game_id": GAME_ID
}
```

REQUIREMENTS:

This project uses sqlite so you will need that to be installed.

The python deps are in requirements.txt

Things that I would normally do but did not have time:
* Test driven dev. Normally I always start with tests. I would add unit tests for helper functions and route tests for the API endpoints, checking all aspects of the endpoint functionality, error responses to incorrect json structure in request body, status codes for both errors and successful requests. etc. 
* Pull out repeated code into functions, namely the checks for user and game.
* Add better handling for when the server is unable to find a word before timeout.
* structure the code better, all functions interacting with DB should be in a controller module.
* Add better handling for db session when something fails we should roll back the session and not commit. There is currently a weakness in /game/word endpoint.
* Errors that are returned from the API in json are not consistent. I would make
all errors with a consistent structure and add error codes and messages in a separate
module to be used throughout.
* I would normally start building an API by creating a yml file for the documentation
of the api endpoints, data and errors. This was not done due to time constraints.

# alohi-word-chain
Alohi Word Chain Game

TODO
# 1. add the endpoint to get history
# 2. add the score output at end of game
# 3. add readme to repo with explanation of the status of this project and what can be done to improve

#JRF TODO, add failure handling... we should pass in the list of words in the history
# so that they can be checked against the result... if we cannot get a word that is not
# already in the list then we timeout and return an empty word.
# if this function returns an empty word then the server causes the game to end with the
# timeout. This code has yet to be added.

# JRF TODO, add handling for extra score if guess was faster than 15 seconds

# JRF TODO add global try, except with finally to complete the session.commit()
# JRF TODO before allowing the user to create a new game, check if there is a game
# already ongoing.


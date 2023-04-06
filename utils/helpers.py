
import random
from venv import logger
# Install NLTK's corpus data
import nltk
from nltk.corpus import words
english_words = set(words.words())


#JRF TODO, add failure handling... if we cannot get a word that is not
# already in the list before the timeout then return an empty word.
# if this function returns an empty word then the server causes the game to end with the
# timeout. This code has yet to be added.
def generate_random_word(starting_letter, previous_words):
    # Try 5 times to find a good word
    word = ""
    score = 0
    timeout = 10000
    count = 5 #we could make a difficulty level and use that.
    while True:
        timeout-=1
        new_word = random.choice(list(english_words))
        if count > 0 and \
            timeout and \
            new_word.startswith(starting_letter) and \
            new_word not in previous_words:
            if word == "" or score < calculate_score(new_word):
                word = new_word
                count -= 1
        elif count == 0:
            return word


def calculate_score(word, fast_bonus):
    score = 0
    for char in word:
        if char in 'aeiou':
            score += 2
        elif char.isalpha():
            score += 1
    return score * 1.5 if fast_bonus else 1

def generate_result(game):
    logger.debug(game)
    winner = "user" if game.user_score > game.server_score else "server" if game.server_score > game.user_score else "draw"
    return {"scores":{"user":game.user_score, "server": game.server_score, "winner": winner}},200


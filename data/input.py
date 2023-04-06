class NewGameData:
    def __init__(self, email):
        self.email = email

class NewWordData:
    def __init__(self, email, game_id, word):
        self.email = email
        self.game_id = game_id
        self.word = word

class EndGameData:
    def __init__(self, email, game_id):
        self.email = email
        self.game_id = game_id

class GameHistoryData:
    def __init__(self, email, game_id):
        self.email = email
        self.game_id = game_id

class NewGameData:
    def __init__(self, email, theme):
        self.email = email
        self.theme = theme

class NewWordData:
    def __init__(self, email, game_id, word):
        self.email = email
        self.game_id = game_id
        self.word = word

class GameId:
    def __init__(self, email, id):
        self.email = email
        self.id = id

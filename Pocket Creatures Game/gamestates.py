# completed
class GameState:
    def __init__(self, game):
        self.game = game

    def events(self, events):
        raise NotImplementedError

    def update(self, screen):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError
    

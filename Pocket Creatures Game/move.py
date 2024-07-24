import pygame

class Move(pygame.sprite.Sprite):

    def __init__(self, name, type, power, accuracy, image = None):
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy

        self.image = image
        if self.image is not None:
            self.rect = image.get_rect()

    def use(self):
        pass

MOVES = {
    "None"            : Move("NULL", "NONE", 0, 0),
    "Body Slam"       : Move("Body Slam", "Normal", 40, 100),
    "Perfect Cut"     : Move("Perfect Cut", "Normal", 70, 80),

    "Water Gun"       : Move("Water Gun", "Water", 60, 100),
    "Water Pump"      : Move("Water Pump", "Water", 70, 90),
    "Flood"           : Move("Flood", "Water", 80, 80),

    "Ember"           : Move("Flame Throw", "Fire", 60, 90),
    "Flamethrower"    : Move("Flamethrower","Fire", 70, 80),
    "Conflagration"   : Move("Conflagration", "Fire", 80, 70),

    "Cuting Leaves"   : Move("Cutting Leafes", "Grass", 60, 90),
    "Root Knock"      : Move("Root Knock", "Grass", 70, 80),
    "Power of Nature" : Move("Power of Nature", "Grass", 80, 80),

    "Stone Throw"     : Move("Stone Throw", "Stone", 60, 90),
    "Executor"        : Move("Executor",  "Stone", 120, 60),

    "Areal Cut"       : Move("Areal Cut", "Flying", 60, 90),
    "Bird Dash"       : Move("Bird Dash", "Flying", 80, 80),
    "Pick"            : Move("Pick", "Flying", 40, 100)
}
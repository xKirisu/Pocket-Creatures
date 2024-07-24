import pygame
import random

from variables import *
from ui import *


class Block(pygame.sprite.Sprite):
    def __init__(self, texture):
        super().__init__()
        self.image = texture
        self.rect = self.image.get_rect()

    def put(self, position):
        self.rect.topleft = position

    def interact(self, game):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def copy(self):
        return self.__class__(self.image)

class Grass(Block):
    def __init__(self, texture):
        super().__init__(texture)

    def interact(self, game):
        super().interact(game)
        if self.rect.collidepoint(game.player.rect.center) and (game.player.moveup or game.player.movedown or game.player.moveleft or game.player.moveright) and game.trainer.creatures.sprites()[0].fainted == False:
            if random.randint(1, 100) > 90:
                game.is_encountered = True
        

class Collided(Block):
    def __init__(self, texture):
        super().__init__(texture)

    def interact(self, game):
        super().interact(game)
        
        if pygame.sprite.collide_rect(game.player, self):
            if game.player.moveup:
                game.player.rect.move_ip([0, game.player.move_speed])
            if  game.player.movedown:
                game.player.rect.move_ip([0, -game.player.move_speed])
            if game.player.moveleft:
                game.player.rect.move_ip([game.player.move_speed, 0])
            if game.player.moveright:
                game.player.rect.move_ip([-game.player.move_speed, 0])

class NPC(Collided):
    def __init__(self, texture, dialog = ""):
        super().__init__(texture)
        self.my_dialog = dialog
        self.effect = self.dummy

    def dummy(self, game):
        print("You execute dummy")
        
    def interact(self, game):

        if pygame.sprite.collide_rect(game.player, self):
            game.on_dialog = True
            game.dialog_start = pygame.time.get_ticks()
            game.dialog_text_text = self.my_dialog
            self.effect(game)
            
        super().interact(game)

    def draw(self, screen):
        super().draw(screen)

        self.function()



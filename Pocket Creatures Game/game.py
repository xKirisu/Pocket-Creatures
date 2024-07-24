import random
import pygame
import sys
import os

from trainer import Trainer
from trainer import Player

from variables import *
from menu import *

from move import *


class Game():
    # global flags
    is_encountered = False
    combat_screen_refresh = False
    on_dialog = False
    end_game = False

    # trainer and player
    trainer = Trainer()
    player = Player(IMAGES["PLAYER"], (WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

    # set sound players
    ambient_sound = SoundCG(-1)
    effect_sound = SoundCG(0)

    # dialog varables
    dialog_start = 0
    dialog_end = 650
    dialog_text_text = ""

    pygame.display.set_icon(IMAGES["ICO"])

    def __init__(self):
        self.state = Menu(self)

    def changestate(self, new_state):
        self.state = new_state

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            self.state.events(events)

            self.state.update(screen)

            self.state.draw(screen)
            
            if self.combat_screen_refresh == False:
                pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        sys.exit()
        
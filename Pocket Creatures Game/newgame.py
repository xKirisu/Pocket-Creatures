# complete
import pygame
import sys
import copy

from variables import *
from onmap import *
from ui import *

from move import MOVES
from creature import BESTIARY

class NewGame(GameState):

    
    def __init__(self, game):
        super().__init__(game)


        textgap = 92

        # clear list after win and new game
        cr = [self.game.trainer.creatures.sprites()]
        self.game.trainer.creatures.remove(cr)
        self.game.trainer.creaturedex.clear()
        self.game.player.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        # starters
        self.roosty = BESTIARY["Roosty"].copy()
        self.shelly = BESTIARY["Shelly"].copy()
        self.trunky = BESTIARY["Trunky"].copy()

        
        for index in range(len(self.roosty.move)):
            if index == 0:
                self.roosty.move[index] = MOVES["Body Slam"]
            else:
                self.roosty.move[index] = MOVES["None"]

        for index in range(len(self.shelly.move)):
            if index == 0:
                self.shelly.move[index] = MOVES["Body Slam"]
            else:
                self.shelly.move[index] = MOVES["None"]

        for index in range(len(self.trunky.move)):
            if index == 0:
                self.trunky.move[index] = MOVES["Body Slam"]
            else:
                self.trunky.move[index] = MOVES["None"]

        # buttons 
        choose_height = WINDOW_HEIGHT//2 - textgap/6
        self.choose_fire_button = Button("", WHITE, LIGHTGRAY, WINDOW_WIDTH//4, choose_height, 128, 128, sec_color=FIRERED)
        self.choose_water_button = Button("", WHITE, LIGHTGRAY, WINDOW_WIDTH//2, choose_height, 128, 128, sec_color=WATERBLUE)
        self.choose_grass_button = Button("", WHITE, LIGHTGRAY, WINDOW_WIDTH - WINDOW_WIDTH//4, choose_height, 128, 128, sec_color=LEAFGREEN)

        # names
        self.fire_name = Text(self.roosty.name, DARK, self.choose_fire_button.rect.centerx, self.choose_fire_button.rect.centery + textgap)
        self.water_name = Text(self.shelly.name, DARK, self.choose_water_button.rect.centerx, self.choose_water_button.rect.centery + textgap)
        self.grass_name = Text(self.trunky.name, DARK, self.choose_grass_button.rect.centerx, self.choose_grass_button.rect.centery + textgap)

        # types text
        self.fire_type_text = Text(self.roosty.type, FIRERED, self.fire_name.rect.centerx, self.fire_name.rect.centery + textgap/2)
        self.water_type_text = Text(self.shelly.type, WATERBLUE, self.water_name.rect.centerx, self.water_name.rect.centery + textgap/2)
        self.grass_type_text = Text(self.trunky.type, LEAFGREEN, self.grass_name.rect.centerx, self.grass_name.rect.centery + textgap/2)

        # initalize creatures
        self.roosty.increase_scale(2)
        self.shelly.increase_scale(2)
        self.trunky.increase_scale(2)
        
        self.roosty.set_position(self.choose_fire_button.rect.center)
        self.shelly.set_position(self.choose_water_button.rect.center)
        self.trunky.set_position(self.choose_grass_button.rect.center)

        # Text
        self.choose_your_first_creature_text = Text("Choose your first creature", BLACK, WINDOW_WIDTH//2, textgap, font_size=68, font_family="Segoe UI Semibold")


    def events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # select starter
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.choose_fire_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.roosty.restore_scale()
                    self.game.trainer.add_creature(self.roosty)
                    self.game.changestate(OnMap(self.game))
                if self.choose_water_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.shelly.restore_scale()
                    self.game.trainer.add_creature(self.shelly)
                    self.game.changestate(OnMap(self.game))
                if self.choose_grass_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.trunky.restore_scale()
                    self.game.trainer.add_creature(self.trunky)
                    self.game.changestate(OnMap(self.game))

    def update(self, screen):
        pass

    def draw(self, screen):
        screen.fill(WHITE)

        self.choose_your_first_creature_text.draw(screen)

        # draw buttons
        self.choose_fire_button.draw(screen, pygame.mouse.get_pos())
        self.choose_water_button.draw(screen, pygame.mouse.get_pos())
        self.choose_grass_button.draw(screen, pygame.mouse.get_pos())

        # draw creatures
        self.roosty.draw(screen)
        self.shelly.draw(screen)
        self.trunky.draw(screen)

        # draw names
        self.fire_name.draw(screen)
        self.water_name.draw(screen)
        self.grass_name.draw(screen)

        # draw types
        self.fire_type_text.draw(screen)
        self.water_type_text.draw(screen)
        self.grass_type_text.draw(screen)
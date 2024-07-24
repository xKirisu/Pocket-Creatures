import pygame
import sys


from gamestates import *
from variables import *
from ui import *
from creature import *
from newgame import NewGame
#from onmap import OnMap


class Menu(GameState):
    def __init__(self, game):
        super().__init__(game)

        gap = 120
        top_buttons_gap = 50

        self.title_text = Text("POCKET CREATURES", LIGHTNINGYELLOW, WINDOW_WIDTH//2, gap/2, 82)

        self.start_button = Button("New Game", DARK, LIGHTGRAY, WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - gap + top_buttons_gap, 250, 100, 42, sec_color=LIGHTNINGYELLOW, font_family="Calibri")
        self.load_button = Button("Continue", DARK, LIGHTGRAY, WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + top_buttons_gap, 250, 100, 42, sec_color=LIGHTNINGYELLOW, font_family="Calibri")
        self.exit_button = Button("Exit", DARK, LIGHTGRAY, WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + gap + top_buttons_gap, 250, 100, 42, sec_color=LIGHTNINGYELLOW, font_family="Calibri")
        
        # prep decoration creatures
        self.decor_creature_1 = BESTIARY["Oinker"].copy()
        self.decor_creature_1.flip()

        self.decor_creature_2 = BESTIARY["Shelly"].copy()

        self.decor_creature_1.increase_scale(4)
        self.decor_creature_2.increase_scale(4)

        decor_y = WINDOW_HEIGHT - WINDOW_HEIGHT//5
        decor_x_1 = WINDOW_WIDTH//10
        decor_x_2 = WINDOW_WIDTH - WINDOW_WIDTH//10

        decor_pos_1 = pygame.rect.Rect(decor_x_1, decor_y, 0, 0)
        decor_pos_2 = pygame.rect.Rect(decor_x_2, decor_y, 0, 0)

        self.decor_creature_1.set_position(decor_pos_1.center)
        self.decor_creature_2.set_position(decor_pos_2.center)

        self.game.ambient_sound.play("MENU", 0.05)


    def events(self, events):
         for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.game.changestate(NewGame(self.game))
                elif self.load_button.rect.collidepoint(pygame.mouse.get_pos()):
                    if self.load_game():
                        from onmap import OnMap
                        self.game.changestate(OnMap(self.game))
                    else:
                        self.game.changestate(NewGame(self.game))
                    pass
                elif self.exit_button.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                

    def load_game(self):
        with open(SAVE_FILE, 'r') as file:
            for line in file:
                attributes = line.strip().split(';')
                self.game.trainer.load_creature(attributes)
        if len(self.game.trainer.creatures) >= 1:
            return True
        else:
            return False


    def update(self, screen):
        pass
    
    def draw(self, screen):
        screen.fill(WHITE)
        self.title_text.draw(screen)

        self.start_button.draw(screen, pygame.mouse.get_pos())
        self.load_button.draw(screen, pygame.mouse.get_pos())
        self.exit_button.draw(screen, pygame.mouse.get_pos())

        self.decor_creature_1.draw(screen)
        self.decor_creature_2.draw(screen)
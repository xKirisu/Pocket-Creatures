import pygame
import sys
from gamestates import GameState
from ui import *

class EndScreen(GameState):
    def __init__(self, game):
        super().__init__(game)
        standard = 16
        withcounter = 24
        gap = 48
        self.gapper = WINDOW_HEIGHT
        self.game = game
        self.complete_dex_info_1 = Text("You complete creature dex.", WHITE, WINDOW_WIDTH//2, self.gapper + standard + withcounter * 0)
        self.complete_dex_info_2 = Text("This path has been completed but your journey continues", WHITE, WINDOW_WIDTH//2, self.gapper + standard + withcounter * 1)

        self.project = Text("This game was made to pass the course Programowanie Obiektowe 2 :D", WHITE, WINDOW_WIDTH//2, self.gapper + standard + withcounter * 2 + gap * 1)
        self.proggrammer = Text("Programmer: Krystian Opałacz", WHITE,  WINDOW_WIDTH//2, self.gapper + standard + withcounter * 3 + gap * 1)

        self.textures1 = Text("Creature textures: Pixel Frog", WHITE,  WINDOW_WIDTH//2, self.gapper + standard + withcounter * 4 + gap * 2)
        self.textures2 = Text("Map textures: Zed", WHITE,  WINDOW_WIDTH//2, self.gapper + standard + withcounter * 5 + gap * 2)
        self.music = Text("Sounds from pixabay", WHITE,  WINDOW_WIDTH//2, self.gapper + standard + withcounter * 6 + gap * 2)
        self.startmenumusic = Text("Main menu music by Geoffrey Burch from Pixabay", WHITE,  WINDOW_WIDTH//2, self.gapper + standard + withcounter * 7 + gap * 2)
        

        self.thanksfp = Text("Thanks for playing", WHITE,  WINDOW_WIDTH//2, self.gapper + standard + withcounter * 8 + gap * 3)
        self.theend = Text("THE END", WHITE,  WINDOW_WIDTH//2, self.gapper + standard + withcounter * 10 + gap * 3)

        self.end_text = [self.complete_dex_info_1, self.complete_dex_info_2, self.project, self.proggrammer, self.textures1, self.textures2, self.music, self.startmenumusic, self.thanksfp, self.theend]
    
    def events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, screen):
        for text in self.end_text:
            text.rect.y -= 1

        if self.theend.rect.y < -32:
            self.game.end_game = False
            from menu import Menu
            self.game.changestate(Menu(self.game))

    def draw(self, screen):
        screen.fill(BLACK)
        for text in self.end_text:
            text.draw(screen)

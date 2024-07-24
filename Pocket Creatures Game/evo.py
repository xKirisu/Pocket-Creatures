import pygame
import sys
from gamestates import GameState
from ui import *
from creature import *
class Evo(GameState):
    def __init__(self, game):
        super().__init__(game)

        self.game.ambient_sound.play("EVOLVE", 0.25)

        self.game.is_encountered = False
        self.game.combat_screen_refresh = False

        self.creature = self.game.trainer.creatures.sprites()[0]
        previous_form_name = self.creature.name.upper()
        next_form_name = self.creature.nextform.upper()
        self.name = self.creature.nextform

        center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        self.text = Text("Your creature is evolving!", BLACK, WINDOW_WIDTH//2, 128, 64)

        self.previous = Element(IMAGES[previous_form_name], center)
        self.previous.image = pygame.transform.scale(self.previous.image, (self.previous.image.get_width() * 4, self.previous.image.get_height() * 4))
        self.previous.rect = self.previous.image.get_rect()
        self.previous.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        self.next = Element(IMAGES[next_form_name], center)
        self.next.image = pygame.transform.scale(self.next.image, (self.next.image.get_width() * 4, self.next.image.get_height() * 4))
        self.next.rect = self.previous.image.get_rect()
        self.next.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        self.size = 0
        self.evolved = False

        # adding to creaturedex with delete old controll
        creature_name_counter = 0
        for creature_name in self.game.trainer.creaturedex:
            if creature_name == previous_form_name:
                creature_name_counter += 1
        
        if creature_name_counter == 1:
            self.game.trainer.creaturedex.remove(previous_form_name)

        self.game.trainer.creaturedex.add(next_form_name)

        for creature_name in self.game.trainer.creaturedex:
            print(creature_name)

        self.game.trainer.text_creaturedex.text = f"Creaturedex: {len(self.game.trainer.creaturedex)}/19"

    def events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self, screen):
        
        if self.evolved == False:
            self.size += 0.5
            if self.size > 100:
                self.evolved = True
        else:
            self.size -= 0.5
        
        if self.size <= -32 and self.evolved:
           self.game.trainer.creatures.sprites()[0].evolve()
           from onmap import OnMap
           self.game.changestate(OnMap(self.game))

    def draw(self, screen):
        screen.fill(WHITE)
        self.text.draw(screen)

        if self.evolved:
            self.next.draw(screen)
        else:
            self.previous.draw(screen)
        pygame.draw.circle(screen, LIGHTGRAY, (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), self.size)

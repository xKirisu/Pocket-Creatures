import pygame
import sys
import random
from variables import *
from gamestates import *
from blocks import *



class OnMap(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.game.is_encountered = False
        self.game.combat_screen_refresh = False
        

        # blackscreening
        self.blackscreen = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
        self.blackalpha = 0
        self.blackalpha_darking = 0.5
        self.blackalpha_intensity = 0

        # dialog varables
        self.dialog_text = Text(game.dialog_text_text, WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT-72)

        # map preparation
        wall = Collided(IMAGES["WALL"])
        tree = Collided(IMAGES["TREE"])
        floor = Block(IMAGES["FLOOR"])
        grass = Grass(IMAGES["GRASS"])

        proffesor = NPC(IMAGES["PROFFESOR"], "Hello trainer. Im proffesor Walnut. (game was saved)")
        nurse = NPC(IMAGES["NURSE"], "Your creatures were healed")

        self.blocks_dic = {
            (102, 57, 49): wall,
            (106, 190, 48): tree,
            (238, 195, 154): floor,
            (153, 229, 80): grass,
            (215, 123, 186): nurse,
            (118, 66, 138): proffesor
        }

        # Map generator
        image = IMAGES["MAP"]
        map_size = map_x, map_y = image.get_size()
        block_size_y = 32
        block_size_x = 32
        self.map_main = pygame.sprite.Group()

        for y in range(map_y):
            for x in range(map_x):
                color = image.get_at((x, y))[:3]
                if color in self.blocks_dic:
                    block = self.blocks_dic[color].copy()
                    if isinstance(block, NPC):
                        block.my_dialog = self.blocks_dic[color].my_dialog
                        if color == (215, 123, 186):
                            block.effect = game.trainer.heal_all
                        elif color == (118, 66, 138):
                            block.effect = self.save_game
                        else:
                            block.effect = block.dummy()
                    block.put([x * block_size_x, y * block_size_y])
                    self.map_main.add(block)
        

        # music preparation
        self.game.ambient_sound.play("IDLEMAP", 0.025)

    def events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.game.player.get_event(event)

            self.game.trainer.list_move(pygame.key.get_pressed())
            


    def update(self, screen):

        if self.game.is_encountered or self.game.end_game:
            self.blackalpha_intensity += self.blackalpha_darking/2
            self.blackalpha += self.blackalpha_darking + self.blackalpha_intensity
        else:
            if self.game.on_dialog == False:
                self.game.player.action()

        if self.blackalpha >= 255:
            if self.game.end_game:
                from endblackscreen import EndScreen
                self.game.changestate(EndScreen(self.game))
            else:
                from newcombat import Combat
                self.game.changestate(Combat(self.game))
          
        
        for block in self.map_main:
            block.interact(self.game)

        if self.game.on_dialog:
            self.dialog_time = pygame.time.get_ticks()
            self.dialog_text.text = self.game.dialog_text_text
            self.dialog_text.update()
            
            if self.dialog_time > self.game.dialog_start + self.game.dialog_end:
                self.game.on_dialog = False


        

    def draw(self, screen):

        screen.fill(GRASSYGREEN)
        self.map_main.draw(screen)

        self.game.player.draw(screen)


        self.game.trainer.draw_list(screen)

        
        if self.game.on_dialog:
            pygame.draw.rect(screen, PANNELBLUE, pygame.Rect(8, WINDOW_HEIGHT - 132, WINDOW_WIDTH - 16, 128))
            self.dialog_text.draw(screen)

        if self.game.is_encountered or self.game.end_game:
            self.blackscreen.fill((0, 0, 0, self.blackalpha))
            screen.blit(self.blackscreen, (0, 0))
            


    def save_game(self, game):
        self.game.effect_sound.play("SAVE", 0.25)
        
        with open(SAVE_FILE, "w") as file:
            for creature in game.trainer.creatures:
                file.write(creature.saveme() + '\n')

        if len(game.trainer.creaturedex) == 19:
            game.end_game = True



             

   
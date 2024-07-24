import pygame
from ui import *
from variables import *

import copy
class Trainer():

    def __init__(self):
        self.creatures = pygame.sprite.Group()
        self.creaturedex = set()

        for creature in self.creatures:
            self.creaturedex.add(self.creatures.name)

        # initalize draw list background
        self.black_block_size = (180, 40)
        self.black_block = pygame.Surface(self.black_block_size, pygame.SRCALPHA)
        self.black_block.fill((BLACK[0], BLACK[1], BLACK[2], 192)) 

        # initalize list drawing objects
        self.text_name = Text("", WHITE, 0, 0, 28)
        self.text_level = Text("", WHITE, 0, 0, 24)

        self.hpbar = HPBar(105, 8)

        # initalize creaturedex info
        text_creaturedex_position = (112, WINDOW_HEIGHT- 16)
        self.text_creaturedex = Text(f"Creaturedex: {len(self.creaturedex)}/18", WHITE, text_creaturedex_position[0], text_creaturedex_position[1], 32)
        
        self.block_creaturedex_position = (self.text_creaturedex.rect.topleft[0]-8,self.text_creaturedex.rect.topleft[1]-6)
        self.block_creaturedex = pygame.Surface((208, 32), pygame.SRCALPHA)
        self.block_creaturedex.fill((BLACK[0], BLACK[1], BLACK[2], 192)) 

    def add_creature(self, creature, current_hp = None):
        
        self.creaturedex.add(creature.name)
        copy_creature = creature.copy()
        if current_hp is not None:
            copy_creature.hp = current_hp
        self.creatures.add(copy_creature)

        self.text_creaturedex.text = f"Creaturedex: {len(self.creaturedex)}/19"

    def heal_all(self, game):
        for creature in self.creatures:
            creature.hp = creature.maxhp
            creature.fainted = False
        game.effect_sound.play("HEALING", 0.03)

    def draw_creaturedex_counter(self, screen):
        screen.blit(self.block_creaturedex, self.block_creaturedex_position)

        self.text_creaturedex.update()
        self.text_creaturedex.draw(screen)

    def draw_list(self, screen):
        self.draw_creaturedex_counter(screen)
        for index, creature in enumerate(self.creatures):
            if index == 4:
                position_rect = (8, 8 + index * (self.black_block_size[1] + 8))
                screen.blit(self.black_block, position_rect)

                position_text_name = (position_rect[0] + self.black_block_size[0]//2, position_rect[1] + self.black_block_size[1]//2)
                self.text_name.cx, self.text_name.cy = position_text_name
                self.text_name.text = "More Creatures"
                self.text_name.update()
                self.text_name.draw(screen)
            elif index > 4:
                continue
            else:
                position_rect = (8, 8 + index * (self.black_block_size[1] + 8))
                position_creature = (position_rect[0] + 25, position_rect[1] + 12)

                position_text_name = (position_rect[0] + self.black_block_size[0]//2, position_rect[1] + 14)
                position_text_level = (position_rect[0] + self.black_block_size[0] - 32, position_text_name[1])

                position_hpbar = (position_rect[0] + self.black_block_size[0]//3, position_rect[1] + 28)


                
                screen.blit(self.black_block, position_rect)

                self.text_name.cx, self.text_name.cy = position_text_name
                self.text_name.text = creature.name
                self.text_name.update()
                self.text_name.draw(screen)

                self.text_level.cx, self.text_level.cy = position_text_level
                self.text_level.text = "LV: " + str(creature.level)
                self.text_level.update()
                self.text_level.draw(screen)



                if creature.hp > 0:
                    hp = creature.hp/creature.maxhp * 100
                    self.hpbar.new_position(position_hpbar)
                    self.hpbar.update(hp)
                    self.hpbar.draw(screen)
                else:
                    pass

                creature_icon = Icon(IMAGES[creature.name.upper()])
                creature_icon.rect.center = position_creature
                creature_icon.draw(screen)


    def list_move(self, key):
        creature_list = list(self.creatures)

        if key[pygame.K_UP]:
            creature_list = creature_list[1:] + creature_list[:1]
        elif key[pygame.K_DOWN]:
            creature_list = creature_list[-1:] + creature_list[:-1]
        
        self.creatures.empty()
        self.creatures.add(creature_list)


    def load_creature(self, attributes):
        from creature import Creature
        from move import MOVES
        level = int(attributes[0])
        name = attributes[1]
        attack = int(attributes[2])
        special = int(attributes[3])
        speed = int(attributes[4])
        defense = int(attributes[5])
        resistance = int(attributes[6])
        maxhp = int(attributes[7])
        hp = int(attributes[8])
        type = attributes[9]
        exp = int(attributes[10])
        maxexp = int(attributes[11])
        actual_scale = float(attributes[12])
        will = int(attributes[13])
        fainted = bool(attributes[14])

        texture = IMAGES[name.upper()]
        move1 = MOVES.get(attributes[15])
        move2 = MOVES.get(attributes[16])
        move3 = MOVES.get(attributes[17])
        move4 = MOVES.get(attributes[18])

        if move1 is None:
            move1 = MOVES["None"]
        if move2 is None:
            move2 = MOVES["None"]
        if move3 is None:
            move3 = MOVES["None"]
        if move4 is None:
            move4 = MOVES["None"]

        nextform = attributes[19]
        if nextform == "None":
            nextform = None


        creature = Creature(texture, name, attack, special, speed, defense, resistance, maxhp, type, level, move1, move2, move3, move4, nextform)
        creature.exp = exp
        creature.maxexp = maxexp
        creature.actual_scale = actual_scale
        creature.will = will
        creature.fainted = fainted

        self.add_creature(creature, hp)

class Player(pygame.sprite.Sprite):
    def __init__(self, texture, position):
        

        self.move_speed = 7.5

        self.moveup = False
        self.movedown = False
        self.moveleft = False
        self.moveright = False


        # animation config
        self.ani_speed = 0.24
        self.actual_frame = 0
        number_of_frames = 24

        frames = []
        self.image = texture

        for i in range(number_of_frames):
            frame = self.image.subsurface(pygame.Rect(i * 32, 0, 32, 32))
            frames.append(frame)

        self.frames_down = frames[0:5]
        self.frames_right = frames[6:12]
        self.frames_up = frames[13:17]
        self.frames_left = frames[18:24]

        self.rect = self.frames_down[0].get_rect()
        self.rect.center = position

        self.image = self.frames_down[0]

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.moveup = True
            if event.key == pygame.K_s:
                self.movedown = True
            if event.key == pygame.K_a:
                self.moveleft = True
            if event.key == pygame.K_d:
                self.moveright = True
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.moveup = False
            if event.key == pygame.K_s:
                self.movedown = False
            if event.key == pygame.K_a:
                self.moveleft = False
            if event.key == pygame.K_d:
                self.moveright = False

    def _animation(self):
        if self.moveup:
            self.actual_frame += self.ani_speed
            if self.actual_frame >= len(self.frames_up):
                self.actual_frame = 0
            self.image = self.frames_up[int(self.actual_frame)]

        elif self.movedown:
            self.actual_frame += self.ani_speed
            if self.actual_frame >= len(self.frames_down):
                self.actual_frame = 0
            self.image = self.frames_down[int(self.actual_frame)]

        elif self.moveleft:
            self.actual_frame += self.ani_speed
            if self.actual_frame >= len(self.frames_left):
                self.actual_frame = 0
            self.image = self.frames_left[int(self.actual_frame)]

        elif self.moveright:
            self.actual_frame += self.ani_speed
            if self.actual_frame >= len(self.frames_right):
                self.actual_frame = 0
            self.image = self.frames_right[int(self.actual_frame)]

        
    def action(self):
        if self.moveup:
            self.rect.move_ip(0, -self.move_speed)
        if self.movedown:
            self.rect.move_ip(0, self.move_speed)
        if self.moveleft:
            self.rect.move_ip(-self.move_speed, 0)
        if self.moveright:
            self.rect.move_ip(self.move_speed, 0)

        # Border collision
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

        self._animation()
    def draw(self, screen):
        screen.blit(self.image, self.rect)


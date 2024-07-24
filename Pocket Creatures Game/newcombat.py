import pygame
import random

import sys

from variables import *
from gamestates import *
from ui import *


from creature import BESTIARY
from move import MOVES

# tyechart table index by [attacker][target]
TYPECHART = [
    [1,  1,   1,   1,   1,    1],
    [1,  0.5, 2,   0.5, 2,    1],
    [1,  0.5, 0.5, 2,   0.5,  2],
    [1,  2,   0.5, 0.5, 2,    1],
    [1,  0.5, 2,   0.5, 1,    2],
    [2,  1,   1,   1,   0.5,  2]
]

# better to use enum but its requires changes in too many space in code
def type_to_index(type):
    if type == "Normal":
        return 0
    elif type == "Water":
        return 1
    elif type == "Fire":
        return 2
    elif type == "Grass":
        return 3
    elif type == "Rock":
        return 4
    elif type == "Flying":
        return 5
    else:
        print("Type name error" + type)
        return 0
        




class Combat(GameState):


    def _platform_init(self):
        platform_scale = 7
        self.platform_image = IMAGES["PLATFORM"]

        platform_width = self.platform_image.get_width() * platform_scale
        platform_height = self.platform_image.get_height() * platform_scale

        self.platform_rect = self.platform_image.get_rect()
        self.platform_image =  pygame.transform.scale(self.platform_image, (platform_width, platform_height))

        self.platform_player_rect = pygame.Rect(PLATFORM_LEFT_GAP, WINDOW_HEIGHT//2, platform_width, platform_height)

        self.platform_enemy_rect = pygame.Rect(WINDOW_WIDTH - (PLATFORM_LEFT_GAP + platform_width), WINDOW_HEIGHT//2 - (PANNEL_HEIGHT + platform_height/2), platform_width, platform_height)
        
        self.hit_sprite = Element(IMAGES["HIT"], (-32,-32))

    def _enemy_initalize(self):
        select_enemy = random.choice(list(BESTIARY.keys())[:14])
        enemy = BESTIARY[select_enemy].copy()

        move_list = list(MOVES.keys())

        selected_moves = [
            name for name in move_list 
            if MOVES[name] is not None and (MOVES[name].type == enemy.type or MOVES[name].type == "Normal")
        ]


        choises = []
        for index in range(4):
            if len(selected_moves) > 0 and (random.randint(1, 10) > 4+index or index == 1):
                name_of_move = random.choice(selected_moves)
                choises.append(MOVES[name_of_move])
                selected_moves.remove(name_of_move)
            else:
                choises.append(MOVES["None"])



        enemy.initalize(choises)

        return enemy

    def _creature_init(self):
        #initalize creatures
        creatures_y_gap = -29 # corrector on platform position

        # initalize enemy
        self.enemy = self._enemy_initalize()

        self.enemy.increase_scale(4)
        self.enemy.set_position((self.platform_enemy_rect.centerx, self.platform_enemy_rect.top + creatures_y_gap))

        # initalize own creatures
        self.own_creature = self.game.trainer.creatures.sprites()[0]
        if self.own_creature.is_fliped == False:
            self.own_creature.flip()
        self.own_creature.increase_scale(4)
        self.own_creature.set_position((self.platform_player_rect.centerx, self.platform_player_rect.top + creatures_y_gap))     
    
    def _light_panel_init(self):
        # initalize light panel
        self.own_panel = Element(IMAGES["LIGHTPANEL"], (WINDOW_WIDTH - 205, WINDOW_HEIGHT - (PANNEL_HEIGHT + 100)))
        self.enemy_panel = Element(IMAGES["LIGHTPANEL"], (205, 100))
       
        # initalize name
        self.name_text_player = Text(self.own_creature.name, WHITE, self.own_panel.rect.left + 16, self.own_panel.rect.y + 28, font_size=58, to_left=True)
        self.name_text_enemy = Text(self.enemy.name, WHITE, self.enemy_panel.rect.left + 16, self.enemy_panel.rect.y + 28, font_size=58, to_left=True)

        #initalize level
        self.level_text_own_creature = Text("LV: " + str(self.own_creature.level), WHITE, self.name_text_player.rect.left + 235, self.name_text_player.rect.centery,  font_size=58)
        self.level_text_enemy = Text("LV: " + str(self.enemy.level), WHITE, self.name_text_enemy.rect.left + 235, self.name_text_enemy.rect.centery,  font_size=58)

        # initalize hpbar
        self.hpbar_own_creature = HPBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, self.own_panel.rect.x + 92,self.own_panel.rect.y + 105, self.own_creature.maxhp)
        self.hpbar_own_creature.update(self.own_creature.hp)
        self.hpbar_enemy = HPBar(HP_BAR_WIDTH, HP_BAR_HEIGHT, self.enemy_panel.rect.x + 92,self.enemy_panel.rect.y + 105, self.enemy.maxhp)
        

    def _button_pref(self, position, text):
        if text != "---":
            return Button(text, WHITE, PANNELDARKBLUE, position[0], position[1], PANNEL_BUTTON_WIDTH, PANNEL_BUTTON_HEIGHT, sec_color=PANNELLIGHTBLUE)
        else:
            return Button(text, WHITE, PANNELDARKBLUE, position[0], position[1], PANNEL_BUTTON_WIDTH, PANNEL_BUTTON_HEIGHT)
        
    def _button_init(self):
        # buttons
        every_button_positions = [
            (PANNEL_BUTTON_WIDTH//2 + 16, WINDOW_HEIGHT - PANNEL_HEIGHT/1.5),
            ((PANNEL_BUTTON_WIDTH//2 + 16)*3.14, WINDOW_HEIGHT - PANNEL_HEIGHT/1.5),
            (PANNEL_BUTTON_WIDTH//2 + 16, WINDOW_HEIGHT - PANNEL_HEIGHT/4),
            ((PANNEL_BUTTON_WIDTH//2 + 16)*3.14, WINDOW_HEIGHT - PANNEL_HEIGHT/4)
        ]
        
        # initalize move buttons
        self.buttons = []
        for index, move in enumerate(self.own_creature.move):
            if move is not None:
                if move.name != "NULL":
                    button = self._button_pref(every_button_positions[index], move.name)
                    self.buttons.append(button)
                else:
                    button = self._button_pref(every_button_positions[index], "---")
                    self.buttons.append(button)
            else:
                print("UNCREATE BUTTON ERROR")

        #initalize normal buttons
        self.button_catch = self._button_pref((WINDOW_WIDTH - (PANNEL_BUTTON_WIDTH//2 + 16), WINDOW_HEIGHT - PANNEL_HEIGHT/1.5), "Catch")
        self.button_run = self._button_pref((WINDOW_WIDTH - (PANNEL_BUTTON_WIDTH//2 + 16), WINDOW_HEIGHT - PANNEL_HEIGHT/4), "Run")

        # initalize info text
        self.info_text = Text("", WHITE, WINDOW_WIDTH//2, WINDOW_HEIGHT - PANNEL_BUTTON_HEIGHT*1.5, 52)
        
    
    
    def __init__(self, game):
        super().__init__(game)
        self.game.combat_screen_refresh = True
        self.waiting = True
        self.actiontype = "combat"

        self._platform_init()
        self._creature_init()
        self._light_panel_init()
        self._button_init()

        self.game.ambient_sound.play("COMBAT", 0.025)

    def events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_run.rect.collidepoint(pygame.mouse.get_pos()):
                    self.actiontype = "run"
                    self.waiting = False
                if self.button_catch.rect.collidepoint(pygame.mouse.get_pos()):
                    self.actiontype = "catch"
                    self.waiting = False

                for index in range(len(self.buttons)):
                    if self.buttons[index].rect.collidepoint(pygame.mouse.get_pos()) and self.buttons[index].text.text != "---":

                        self.waiting = False
                        self.move_action_my = self.own_creature.move[index]
                        self.move_action_en = random.choice([move for move in self.enemy.move if move.name != "NULL"])
                        r1 = random.randint(1,5)
                        r2 = random.randint(1,5)

                        if self.own_creature.speed + r1 > self.enemy.speed + r2:
                            self.first_creature = self.own_creature
                            self.first_move = self.move_action_my

                            self.secound_creature = self.enemy
                            self.secound_move = self.move_action_en
                        else:
                            self.first_creature = self.enemy
                            self.first_move = self.move_action_en

                            self.secound_creature = self.own_creature
                            self.secound_move = self.move_action_my


    def update(self, screen):
        pass


    def _draw_scene(self, screen):

        screen.fill(GLASSGREEN)
           
        pygame.draw.rect(screen, PANNELBLUE, (0, WINDOW_HEIGHT - PANNEL_HEIGHT, WINDOW_WIDTH, PANNEL_HEIGHT))


        # draw enemy
        screen.blit(self.platform_image, self.platform_enemy_rect) 
        self.enemy_panel.draw(screen)
        if self.actiontype != "catch":
            self.enemy.draw(screen)
        self.hpbar_enemy.draw(screen)
        self.name_text_enemy.draw(screen)
        self.level_text_enemy.draw(screen)
    
        # draw player
        screen.blit(self.platform_image, self.platform_player_rect)
        self.own_panel.draw(screen)
        self.own_creature.draw(screen)
        self.hpbar_own_creature.draw(screen)
        self.name_text_player.draw(screen)
        self.level_text_own_creature.draw(screen)

    def draw(self, screen):
        if self.waiting == True:
            self._draw_scene(screen)

            for button in self.buttons:
                button.draw(screen, pygame.mouse.get_pos())

            self.button_catch.draw(screen, pygame.mouse.get_pos())
            self.button_run.draw(screen, pygame.mouse.get_pos())

            pygame.display.flip()
        else:
            if self.actiontype == "catch":
                self._catching(screen)
            elif self.actiontype == "run":
                self._running()
            elif self.actiontype == "combat":
                self.full_action(screen, self.first_creature,self.secound_creature, self.first_move)


                self.full_action(screen, self.secound_creature,self.first_creature, self.secound_move)


                self.waiting = True
            else:
                self.actiontype = "combat"



    def wait(self):
        pygame.time.wait(700)

    def catch_formula(self):
        catch_rate = 140*((self.enemy.maxhp - self.enemy.hp)/self.enemy.maxhp) - (self.enemy.will + random.randint(1, 10) + self.enemy.level)
        if catch_rate >= 50: 
            return True
        else: 
            return False 
        
    def damage_formula(self, attacker, target, move):
        lv_diff = attacker.level - target.level if attacker.level > target.level else 0

        base = (lv_diff)*10 + random.randint(1, 20)
        typemultiper = TYPECHART[type_to_index(move.type)][type_to_index(target.type)]

        

        if move.type in ("Normal", "Stone", "Flying"):
            damage = base + move.power *(1-(target.defense-attacker.attack)*0.1)*typemultiper
        else:
            damage = base + move.power *(1-(target.resistance-attacker.special)*0.1)*typemultiper

        damage = int(damage) * self.hit_chance * self.critical_value

        if damage < 0:
            damage = 0

        return damage
    
    def _catching(self, screen):
        self._draw_scene(screen)

        position = (self.enemy.rect.centerx, self.enemy.rect.centery+32)
        pygame.draw.circle(screen, LIGHTGRAY, position, 64)

        self.info_text.text = "Catching..."

        self.info_text.update()
        self.info_text.draw(screen)

        pygame.display.flip()
        self.wait()
        catchcount = 1
        for catchcount in range(4):
            if self.catch_formula():
                continue
            else:
                self.actiontype = "afthercatch"
                self.info_update_only(screen, self.enemy.name + " broke free")

                self.move_action_en = random.choice([move for move in self.enemy.move if move.name != "NULL"])
                self.full_action(screen, self.enemy, self.own_creature, self.move_action_en)
                self.waiting = True
                break

        if catchcount == 3:
            self.game.effect_sound.play("CATCH", 0.05)

            self._draw_scene(screen)
            pygame.draw.circle(screen, LIGHTNINGYELLOW, position, 64)

            self.info_text.text = "You captured " + self.enemy.name
            self.enemy.restore_scale()
            self.game.trainer.add_creature(self.enemy, self.enemy.hp)

            self.info_text.update()
            self.info_text.draw(screen)
            pygame.display.flip()


            self.wait()
            self._running(True)

    def info_update_only(self, screen, text):
        self._draw_scene(screen)

        self.info_text.text = text

        self.info_text.update()
        self.info_text.draw(screen)

        pygame.display.flip()
        self.wait()

    def _running(self, always_success = False):
        from onmap import OnMap
        if always_success == True:
            self.game.changestate(OnMap(self.game))
        else:
            if random.randrange(1, 20) > 10 - (self.own_creature.level - self.enemy.level):
                self.info_update_only(screen, "Run away safety")

                self.game.changestate(OnMap(self.game))
            else:
                self.info_update_only(screen, "Unsuccess run away")

                self.move_action_en = random.choice([move for move in self.enemy.move if move.name != "NULL"])
                self.full_action(screen, self.enemy, self.own_creature, self.move_action_en)
                self.actiontype = "aftherrun"
                self.waiting = True


    def full_action(self, screen, first_creature, secound_creature, move):
        if first_creature.fainted == False:

            self.hit_chance =  1 if random.randint(1, 100) < move.accuracy else 0
            self.critical_value =  2 if random.randint(1, 100) < 10 else 1

            self.info_action(screen, first_creature, move)
            self.take_action(screen, first_creature, secound_creature, move)
            self.changehpbar_action(screen)
            self.infoafter_action(screen, first_creature, secound_creature, move)

            self.check_fainted(screen)
            


    def check_fainted(self, screen):
        if self.own_creature.fainted == True:
            self.info_update_only(screen, self.own_creature.name + " is unable to fight")
            self._running(True)

        elif self.enemy.fainted == True:
            self.info_update_only(screen, self.enemy.name + " was defeated")
            self.info_update_only(screen, self.own_creature.name + " get " + str(self.enemy.will*4 + 20) + " experience")
            if self.own_creature.levelup(self.enemy.will*4):
                self.info_update_only(screen, self.own_creature.name + " level up")

            if self.own_creature.level >= 12 and self.own_creature.nextform != None:
                from evo import Evo
                self.game.changestate(Evo(self.game))
            else:
                self._running(True)

    def changehpbar_action(self, screen):
        

        self.hpbar_enemy.update(self.enemy.hp)
        self.hpbar_own_creature.update(self.own_creature.hp)

        self._draw_scene(screen)

        self.hpbar_enemy.draw(screen)
        self.hpbar_own_creature.draw(screen)

        pygame.display.flip()
        #self.wait()

    def info_action(self, screen, attacker, move):
        self._draw_scene(screen)

        self.info_text.text = attacker.name + " used " + move.name
        self.info_text.update()
        self.info_text.draw(screen)

        pygame.display.flip()
        self.wait()

    def take_action(self, screen, attacker, target, move):
        self._draw_scene(screen)

        
        damage = self.damage_formula(attacker, target, move)
        target.hurt(damage)

        if damage > 0:
            self.game.effect_sound.play("HURT", 0.03)
            self.hit_sprite.rect.center = target.rect.center
            self.hit_sprite.draw(screen)


        pygame.display.flip()
        self.wait()

    def infoafter_action(self, screen, attacker, target, move):
        self._draw_scene(screen)


        if self.hit_chance == 0:
            self.info_text.text = f"{target.name} avoid attack"
        elif TYPECHART[type_to_index(move.type)][type_to_index(target.type)] == 2:
            self.info_text.text = "It was very effective"
        elif TYPECHART[type_to_index(move.type)][type_to_index(target.type)] == 0.5:
            self.info_text.text = "It is not effective"
        else:
            self.info_text.text = ""

        if self.critical_value == 2 and self.hit_chance == 1:
            if TYPECHART[type_to_index(move.type)][type_to_index(target.type)] == 2:
                self.info_text.text += " and critical"
            elif TYPECHART[type_to_index(move.type)][type_to_index(target.type)] == 0.5:
                self.info_text.text += " but critical"
            else:
                self.info_text.text = "It was critical"

        
        self.info_text.update()
        self.info_text.draw(screen)

        pygame.display.flip()
        self.wait()


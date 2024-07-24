import pygame
import random
from game import IMAGES

from move import Move

class Creature(pygame.sprite.Sprite):
    
    
    def __init__(self, texture, name, attack, special, speed, defense, resistance, hp, type, level = 5, move_1 = None, move_2 = None, move_3 = None, move_4 = None, nextform = None):
        super().__init__()
        self.image = texture

        # actual rect
        self.rect = self.image.get_rect()
        # restoring rect
        self.restore_rect = self.image.get_rect()
        #isfliped
        self.is_fliped = False
        


        # statistics
        self.level = level
        self.name = name
        self.attack = attack
        self.special = special
        self.speed = speed
        self.defense = defense
        self.resistance = resistance
        self.maxhp = hp

        self.hp = self.maxhp

        self.type = type

        self.exp = 0
        self.maxexp = 4 * self.level

        self.actual_scale = 1

        self.will = random.randint(0, 15)
        self.fainted = False

        # moves
        self.move = []
        self.move.append(move_1)
        self.move.append(move_2)
        self.move.append(move_3)
        self.move.append(move_4)

        self.nextform = nextform

    def initalize(self, moves):

        self.level = random.randint(1, 5)
        
        new_moves = []
        for m in moves:
            new_moves.append(m)
        self.move = new_moves

        #ivs 
        ivs_attack = random.randint(0, 3)
        ivs_special = random.randint(0, 3)
        ivs_speed = random.randint(0, 3)
        ivs_defense = random.randint(0, 3)
        ivs_resistance = random.randint(0, 3)
        ivs_hp = random.randint(0, 3)

        self.attack += ivs_attack
        self.special += ivs_special
        self.speed += ivs_speed
        self.defense += ivs_defense
        self.resistance += ivs_resistance
        self.hp += ivs_hp


        
    def _animation(self):
        pass

    def set_position(self, position):
        self.rect.center = position
        
    

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.is_fliped = True

    def increase_scale(self, new_scale):
        self.restore_scale()
        current_width, current_height = self.rect.size
        
        new_width = int(current_width * new_scale)
        new_height = int(current_height * new_scale)

        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        self.rect.size = self.image.get_rect().size

        self.actual_scale = new_scale

    def restore_scale(self):
        if self.actual_scale != 1.0:
            self.image = pygame.transform.scale(self.image, self.restore_rect.size)
            self.rect.size = self.image.get_rect().size
            self.current_scale = 1.0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def copy(self):
        return self.__class__(self.image,self.name,self.attack,self.special,self.speed,
        self.defense,self.resistance,self.maxhp,
        self.type, self.level,
        self.move[0], self.move[1], self.move[2], self.move[3], self.nextform)

    def hurt(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.fainted = True
            self.hp = 0

    def levelup(self, exp):
        isleveled = False
        self.exp += exp
        while self.exp > self.maxexp:
            self.exp -= self.maxexp
            self.level += 1
            self.maxexp = self.level * 4
            isleveled = True

            statistic = random.choice([self.attack, self.special, self.speed, self.defense, self.resistance])
            statistic += 1

        return isleveled

    def saveme(self):
        attributes = [
            self.level, self.name, self.attack, self.special,
            self.speed, self.defense, self.resistance, self.maxhp,
            self.hp, self.type, self.exp, self.maxexp, self.actual_scale,
            self.will, self.fainted, self.move[0].name, self.move[1].name,
            self.move[2].name, self.move[3].name, self.nextform
        ]
        return ';'.join(map(str, attributes))
    
    def evolve(self):
        next_form = BESTIARY[self.nextform]
        self.image = next_form.image
        self.restore_scale()
        self.name  = next_form.name
        self.attack = next_form.attack
        self.special = next_form.special
        self.speed = next_form.speed
        self.defense = next_form.defense
        self.resistance = next_form.resistance
        self.maxhp = next_form.maxhp
        self.nextform = None

# New game nie ustala evolution_level

BESTIARY = {
    "Roosty"   : Creature(IMAGES["ROOSTY"],     "Roosty",   9, 9, 9, 9, 9, 500, "Fire", nextform="Flynky"),
    "Shelly"   : Creature(IMAGES["SHELLY"],     "Shelly",   9, 9, 9, 9, 9, 500, "Water", nextform="Ghosty"),
    "Trunky"   : Creature(IMAGES["TRUNKY"],     "Trunky",   9, 9, 9, 9, 9, 500, "Grass", nextform="Shroomy"),
    "Ducly"    : Creature(IMAGES["DUCLY"],      "Ducly",    3, 6, 5, 2, 3, 600, "Water"),
    "Rumbee"   : Creature(IMAGES["RUMBEE"],     "Rumbee",   4, 7, 6, 3, 4, 400, "Grass"),
    "Rootie"   : Creature(IMAGES["ROOTIE"],     "Rootie",   3, 5, 4, 2, 3, 500, "Grass", nextform="Planty"),
    "Oinker"   : Creature(IMAGES["OINKER"],     "Oinker",   2, 4, 3, 1, 2, 400, "Fire"),
    "Stoneley" : Creature(IMAGES["STONELEY"],   "Stoneley", 5, 8, 7, 4, 5, 800, "Rock", nextform="Horkull"),
    "Speely"   : Creature(IMAGES["SPEELY"],     "Speely",   4, 7, 6, 3, 4, 300, "Normal"),
    "Slummy"   : Creature(IMAGES["SLUMMY"],     "Slummy",   2, 5, 4, 1, 2, 500, "Water"),
    "Sleedar"  : Creature(IMAGES["SLEEDAR"],    "Sleedar",  3, 6, 5, 2, 3, 600, "Flying"),
    "Toto"     : Creature(IMAGES["TOTO"],       "Toto",     1, 3, 2, 1, 1, 300, "Flying"),
    "Zemee"    : Creature(IMAGES["ZEMEE"],      "Zemee",    4, 7, 6, 3, 4, 400, "Normal"),
    "Drillno"  : Creature(IMAGES["DRILLNO"],    "Drillno",  9, 9, 9, 9, 9, 600, "Rock"),
    #
    "Flynky"   : Creature(IMAGES["FLYNKY"],     "Flynky",   16, 16, 9, 9, 16, 600, "Fire"),
    "Ghosty":   Creature(IMAGES["GHOSTY"],      "Ghosty", 18, 21, 21, 18, 19, 700, "Water"),
    "Shroomy":  Creature(IMAGES["SHROOMY"],     "Shroomy", 18, 12, 12, 12, 12, 700, "Grass"),
    "Planty":   Creature(IMAGES["PLANTY"],      "Planty", 6, 10, 8, 4, 6, 600, "Grass"),
    "Horkull":  Creature(IMAGES["HORKULL"],     "Horkull", 10, 16, 14, 8, 10, 600, "Rock")
    #
}
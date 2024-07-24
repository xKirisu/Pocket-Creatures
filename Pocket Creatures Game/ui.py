import pygame
from variables import *
class Text():
    def __init__(self, text, color, cx, cy, font_size = 36, font_family = None, to_left = False):
        self.text = str(text)
        self.color = color
        self.cx = cx
        self.cy = cy
        self.font = pygame.font.SysFont(font_family, font_size)


        self.to_left = to_left

        
        self.update()

    def update(self):
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        if self.to_left:
            self.rect.top = self.cy
            self.rect.left = self.cx
        else:
            self.rect.center = self.cx, self.cy

    def draw(self,screen):
        screen.blit(self.image, self.rect)

class Button():
    def __init__(self, text, text_color, background_color, cx, cy, width, height, font_size = 36, font_family = None, sec_color = None):
            super().__init__()

            self.text = Text(text, text_color, cx, cy, font_size, font_family)
            self.background_color = background_color

            if sec_color != None:
                self.secound_background_color = sec_color
            else:
                self.secound_background_color = self.background_color

            self.rect = pygame.Rect(0,0, width, height)
            self.rect.center = self.text.rect.center

    def draw(self, screen, mouse_position):
        if(self.rect.collidepoint(mouse_position)):   
            screen.fill(self.secound_background_color, self.rect)
        else:
            screen.fill(self.background_color, self.rect)
        self.text.update()
        self.text.draw(screen)


class Icon(pygame.sprite.Sprite):
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Element(pygame.sprite.Sprite):

    def __init__(self, texture, position):
        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.center = position
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class HPBar:
    def __init__(self,  width, height, x = 0, y = 0, max_hp = 100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.current_hp = max_hp

        self.border_color = (DARK)
        self.hp_color = (GRASSYGREEN)

    def update(self, current_hp):
        self.current_hp = current_hp

    def new_position(self, position):
        self.x, self.y = position
        

    def draw(self, surface):
        pygame.draw.rect(surface, self.border_color, (self.x, self.y, self.width, self.height))

        hp_width = (self.current_hp / self.max_hp) * self.width

        if self.current_hp <= self.max_hp * 0.33:
            self.hp_color = FIRERED
        elif self.current_hp <= self.max_hp * 0.66:
            self.hp_color = LIGHTNINGYELLOW
        else:
            self.hp_color = GRASSYGREEN

        hp_rect = pygame.Rect(self.x, self.y, hp_width, self.height)
        pygame.draw.rect(surface, self.hp_color, hp_rect)
import os
import pygame

# window variables
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = (896, 576)
WINDOW_NAME = "Pocket Creatures"

SAVE_FILE = os.path.join(os.getcwd(), "save.txt")

# colors
BLACK = (0,0,0)
DARK = (33,33,33)
WHITE = (255, 255, 255)

LIGHTGRAY = (230, 230, 230)

FIRERED = (200, 0, 0)
LEAFGREEN = (0, 200, 0)
WATERBLUE = (0, 0, 200)
LIGHTNINGYELLOW = (222, 222, 0)

NORMALGRAY = (203,219,252)
FLYINGBLUE = (0, 150, 177)
STONEYGRAY = (64,64,64)

GRASSYGREEN = (150, 230, 80)
GLASSGREEN = (230,255,230)

PANNELBLUE = (49, 88, 117)

PANNELDARKBLUE = (0, 67, 115)
PANNELLIGHTBLUE = (78, 146, 191)

PANNEL_HEIGHT = 140


# combat panel static varables
LIGHTPANNEL_COLOR = (162, 202, 220)
LIGHTPANNEL_WIDTH = WINDOW_WIDTH//2 - 64
LIGHTPANNEL_HEIGHT = WINDOW_HEIGHT//4


PLATFORM_LEFT_GAP = WINDOW_WIDTH//14

PANNEL_BUTTON_HEIGHT = 45
PANNEL_BUTTON_WIDTH = 255


HP_BAR_HEIGHT = 55
HP_BAR_WIDTH = 280

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(WINDOW_NAME)

clock = pygame.time.Clock()

# import textures
path = os.path.join(os.getcwd(), 'imgs')
file_names = os.listdir(path)

IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4].upper()
    #print(image_name)
    IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha()


# import music
path_music = os.path.join(os.getcwd(), 'music')
music_names = os.listdir(path_music)

SOUND = {}
for music_name in music_names:
    sound_name = music_name[:-4].upper()
    SOUND[sound_name] = pygame.mixer.Sound(os.path.join(path_music, music_name))

class SoundCG:
    def __init__(self, isloop=False):
        pygame.mixer.init()
        self.loop = -1 if isloop else 0

    def play(self, name, volume=0.5):
        if self.loop == -1:
            pygame.mixer.stop()
        if name in SOUND:
            sound = SOUND[name]
            sound.set_volume(volume)
            channel = pygame.mixer.find_channel(True)
            channel.play(sound, loops=self.loop)
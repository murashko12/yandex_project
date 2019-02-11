import pygame
import os
import sys




pygame.init()


WIDTH = 400
HEIGHT = 300
FPS = 50
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)


clock = pygame.time.Clock()
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()
 
 
def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

 
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
 
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                 event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)
start_screen()


# окно: "Добро пожаловать" ------------------------------------------------------



# создаём аниамации        ------------------------------------------------------
'''
class AnimatedSprite_of_main_the_main_character(pygame.sprite.Sprite):
    def __init__(self,):
        super().__init__(all_sprites)
        self.frames = []

    


class AnimatedSprite_of_dragon(pygame.sprite.Sprite): # Дракон (BOSS)
    def __init__(self,):


class AnimatedSprite_of_goblin(pygame.sprite.Sprite): # Гоблин 
    def __init__(self,):


class AnimatedSprite_of_gargoyle(pygame.sprite.Sprite): # Гаргулья 
    def __init__(self,):



# I уровень                ------------------------------------------------------



# II уровень               ------------------------------------------------------



# III уровень              ------------------------------------------------------
'''



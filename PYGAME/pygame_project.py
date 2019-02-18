import pygame
import os
import sys


pygame.init()


WIDTH = 1100
HEIGHT = 700
FPS = 50
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)

# окно: "Добро пожаловать" ------------------------------------------------------

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
    intro_text = ["                                                                           B A R B A R I A N"]

 
    fon = pygame.transform.scale(load_image('welcome.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 9, pygame.Color('red'))
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








# создаём анимации        ------------------------------------------------------




# I уровень                ------------------------------------------------------



# II уровень               ------------------------------------------------------



# III уровень              ------------------------------------------------------

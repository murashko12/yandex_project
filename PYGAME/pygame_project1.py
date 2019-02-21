import pygame
import os
import sys
import random


pygame.init()


WIDTH = 1100
HEIGHT = 700
FPS = 50
size = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()

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

player_image = load_image('barbarian_1.png')
 
def start_screen():
    intro_text = [""]
    fen = load_image('header.png')
    fon = pygame.transform.scale(load_image('welcome.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    screen.blit(fen, (330, 30))
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
            if event.type == pygame.KEYDOWN or \
                 event.type == pygame.MOUSEBUTTONDOWN:
                return  1 # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)
start_screen()

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type != '!':
            self.image = tile_images[tile_type]
        else:
            mode = random.randint(1,3)
            self.image = tile_images[str(mode)]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x  - 26, tile_height * pos_y - 35)
        self.x = pos_x
        self.y = pos_y





# создаём анимации        ------------------------------------------------------




# I уровень                ------------------------------------------------------
def load_level(filename):
    filename = "maps_of_levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину    
    max_width = max(map(len, level_map))
 
    # дополняем каждую строку пустыми клетками ('.')    
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))
level = load_level('level_1.txt')

tile_images = {'#': load_image('tiles_007.png'), # тропинка (есть)
               '.': load_image('cobble.png'), # основная дорога (есть)
               '*': load_image('grass.png'), # трава (есть)
               '2': load_image('wall2.jpg'), # стена (есть)
               '1': load_image('wall1.jpg'), # стена (есть)
               '3': load_image('wall3.jpg'), # стена (есть)
               '=': load_image('sund.png'), # сундук 
               'X': load_image('x.png'), # бомба
               '&': load_image('dor2.png'), # дверь 
               'w': load_image('w.png'), # вода (есть)
               't': load_image('t.png'), 
               'T': load_image('tb.png')} # мост
 
tile_width = tile_height = 20

for i in range(len(level)):
    for j in range(len(level[i])):
        if level[i][j] in 'Tt':
            tile = Tile('w', j, i)
            tile1 = Tile(level[i][j], j, i)
        if level[i][j] in '=':
            tile = Tile('.', j, i)
            tile1 = Tile(level[i][j], j, i)
        if level[i][j] in 'X':
            tile = Tile('#', j, i)
            tile1 = Tile(level[i][j], j, i)
        tile = Tile(level[i][j], j, i)
tiles_group.draw(screen)
pygame.display.flip()

play = Player(51, 33)
# II уровень               ------------------------------------------------------



# III уровень              ------------------------------------------------------
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and level[play.y - 1][play.x] in '.Tt#':
                for i in range(4):
                    play.rect.y -= 4
                    play.image = load_image('barbarian_1_walk_00' + str(i +1) + '.png')
                    clock.tick(9)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
                play.rect.y -= 4
                play.image = load_image('barbarian_1.png')
                play.y -= 1
            if event.key == pygame.K_DOWN and level[play.y + 1][play.x] in '.Tt#':
                for i in range(4):
                    play.rect.y += 4
                    play.image = load_image('barbarian_1_walk_00' + str(i +1) + '.png')
                    clock.tick(9)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
                play.rect.y += 4
                play.image = load_image('barbarian_1.png')
                play.y += 1
            if event.key == pygame.K_LEFT and level[play.y][play.x - 1] in '.Tt#':
                for i in range(4):
                    play.rect.x -= 4
                    play.image = load_image('barbarian_1_walk_00' + str(i +1) + '.png')
                    clock.tick(9)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
                play.rect.x -= 4
                play.image = load_image('barbarian_1.png')
                play.x -= 1
            if event.key == pygame.K_RIGHT and level[play.y][play.x + 1] in '.Tt#':
                for i in range(4):
                    play.rect.x += 4
                    play.image = load_image('barbarian_1_walk_00' + str(i +1) + '.png')
                    clock.tick(9)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
                play.rect.x += 4
                play.image = load_image('barbarian_1.png')
                play.x += 1
            if event.key == pygame.K_a:
                for i in range(3):
                    play.image = load_image('barbarian_1_attack_00' + str(i + 1) + '.png')
                    clock.tick(9)
                    tiles_group.draw(screen)
                    player_group.draw(screen)
                    pygame.display.flip()
                play.image = load_image('barbarian_1.png')
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

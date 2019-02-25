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
sol = 1
lev1 = False
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
    text_coord = 40
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
key_image = load_image('key.png')
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type != '!':
            self.image = tile_images[tile_type]
        else:
            mode = random.randint(2,3)
            self.image = tile_images[str(mode)]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
class Key(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = key_image
        self.rect = self.image.get_rect().move(20,40)
        self.x = pos_x
        self.y = pos_y
        self.alive = True
        self.mask = pygame.mask.from_surface(player_image)
        self.intro_text = ["x 0"]
        self.text_coord = 40
        self.font = pygame.font.Font(None, 30)
        for line in self.intro_text:
            string_rendered = self.font.render(line, 9, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            self.text_coord = 40
            intro_rect.top = self.text_coord
            intro_rect.x = 25
            screen.blit(string_rendered, intro_rect)
    def update(self):
        for line in self.intro_text:
            string_rendered = self.font.render(line, 9, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            self.text_coord = 40
            intro_rect.top = self.text_coord
            intro_rect.x = 25
            screen.blit(string_rendered, intro_rect)
        if level[self.y][self.x] == '&':
            self.intro_text = ['x 0']
key = Key(20,20)
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x  - 26, tile_height * pos_y - 35)
        self.x = pos_x
        self.y = pos_y
        self.alive = True
        self.mask = pygame.mask.from_surface(player_image)
    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        for i in range(len(garg)):
            if pygame.sprite.collide_mask(self, garg[i].ice) != None and self.image not in [load_image('barbarian_1_attack_00' + str(i + 1) + 'R.png') for i in range(3)] and self.image not in [load_image('barbarian_1_attack_00' + str(i + 1) + '.png') for i in range(3)]:
                self.alive = False
        if level[self.y][self.x] == 'o':
            self.alive = False
        if level[self.y][self.x] == '=':
            key.intro_text = ['x 1']
        
class Gargoyle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direct, per):
        super().__init__(player_group, all_sprites)
        self.image = garg_image[0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x  - 26, tile_height * pos_y - 35)
        self.x = 1
        self.alive = True
        self.alive2 = True
        self.d = direct
        self.per = per
        self.ice = Projectile(pos_x, pos_y, direct)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.mask = pygame.mask.from_surface(player_image)
    def update(self):
        if self.alive is True:
            self.x += 1
            self.image = garg_image[self.x%4]
            self.mask = pygame.mask.from_surface(player_image)
        if pygame.sprite.collide_mask(self, play) != None and self.alive is True:
            self.alive = False
        if self.alive is False and self.alive2 is True:
            for i in range(7):
                self.image = load_image('gargoyle_die_00' + str(i + 1) + '.png')
                tiles_group.draw(screen)
                player_group.draw(screen)
                pygame.display.flip()
                clock.tick(9)
            self.alive2 = False
        if self.x == self.per:
            self.ice.rect =  self.image.get_rect().move(
            tile_width * self.pos_x  - 6, tile_height * self.pos_y - 6)
            self.x%=self.per
        
        
            
class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, d):
        super().__init__(player_group, all_sprites)
        self.image = projectile_image[0 + d*2]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x  - 6, tile_height * pos_y - 6)
        self.x = 1
        self.d = d
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.x += 1
        self.x %= 2
        self.image =projectile_image[self.x%2+self.d*2]
        self.mask = pygame.mask.from_surface(projectile_image[self.x%2+self.d*2])
        if self.d == 0:
            self.rect.x += 4
        if self.d == 1:
            self.rect.x -= 4
        if self.d == 2:
            self.rect.y -= 4
        if self.d == 3:
            self.rect.y += 4
def load_level(filename):
    filename = "maps_of_levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]   
    max_width = max(map(len, level_map))  
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))
level = load_level('level_1.txt')
tile_images = {'#': load_image('tiles_007.png'), # тропинка (есть)
               '.': load_image('cobble.png'), # основная дорога (есть)
               '*': load_image('grass.png'), # трава (есть)
               '2': load_image('wall2.jpg'), # стена (есть)
               '0': load_image('wall1.jpg'), # стена (есть)
               '3': load_image('wall3.jpg'), # стена (есть)
               '=': load_image('sund.png'), # сундук 
               'X': load_image('x.png'), # бомба
               '&': load_image('dor.jpg'), # дверь 
               'w': load_image('w.png'), # вода (есть)
               't': load_image('t.png'), 
               'T': load_image('tb.png'),
               'o': load_image('lava.png'),
               '@': load_image('lest.png')} # мост
garg_image = [load_image('gargoyle_fly_00' + str(i) + '.png') for i in range(1,5)]
projectile_image = [load_image('iceball_00' + str(i) + '.png') for i in range(1,3)]
projectile_imageR = [load_image('iceball_00' + str(j) + 'R.png') for j in range(1,3)]
projectile_imageRUP = [load_image('iceball_00' + str(j) + 'RUP.png') for j in range(1,3)]
projectile_imageRDOWN = [load_image('iceball_00' + str(j) + 'RDOWN.png') for j in range(1,3)]
projectile_image += projectile_imageR
projectile_image += projectile_imageRUP
projectile_image += projectile_imageRDOWN
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
garg = [Gargoyle(56, 36, 3, 40) , Gargoyle(28, 16, 1, 30), Gargoyle(44, 25, 3, 30), Gargoyle(4, 32, 0, 116)]
running = True
while running:
    if play.alive is True:
        if play.x == 27 and play.y ==0 and lev1 is False:
            player_group.update()
            level = load_level('level_2.txt')
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
            play.rect.y += 680
            play.y = 34
            lev1=True
            key.intro_text = ['x 0']
            for i in garg:
                i.rect.x+=2000
                i.pos_x = 200
                i.pos_y = 200
            garg = [Gargoyle(56, 36, 3, 40), Gargoyle(3, 17, 1, 10) , Gargoyle(8, 10, 3, 55), Gargoyle(13, 16, 2, 40), Gargoyle(12, 27, 0, 20), Gargoyle(28, 1, 3, 55), Gargoyle(30, 14, 1, 30)]
            tiles_group.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
        if play.x == 27 and play.y == 17 and lev1 is True:
            player_group.update()
            level = load_level('level_3.txt')
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
            lev1 = False
            key.intro_text = ['x 0']
            for i in garg:
                i.rect.x+=2000
                i.pos_x = 200
                i.pos_y = 200
            play.rect.x -= 540
            play.x = 0
            tiles_group.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and level[play.y - 1][play.x] in '.Tt#&@=o':
                    if level[play.y - 1][play.x] == '&' and key.intro_text == ['x 1']:
                        if sol == 1:
                            for i in range(4):
                                play.rect.y -= 4
                                play.image = load_image('barbarian_1_walk_00' + str(i +1) + '.png')
                                tiles_group.draw(screen)
                                player_group.draw(screen)
                                pygame.display.flip()
                                player_group.update()
                                clock.tick(15)
                            play.rect.y -= 4
                            play.image = load_image('barbarian_1.png')
                            play.y -= 1
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                        else:
                            for i in range(4):
                                play.rect.y -= 4
                                play.image = load_image('barbarian_1_walk_00' + str(i +1) + 'R.png')
                                tiles_group.draw(screen)
                                player_group.draw(screen)
                                pygame.display.flip()
                                player_group.update()
                                clock.tick(15)
                            play.rect.y -= 4
                            play.image = load_image('barbarian_1R.png')
                            play.y -= 1
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                    elif level[play.y - 1][play.x] != '&':
                        if sol == 1:
                            for i in range(4):
                                play.rect.y -= 4
                                play.image = load_image('barbarian_1_walk_00' + str(i +1) + '.png')
                                tiles_group.draw(screen)
                                player_group.draw(screen)
                                pygame.display.flip()
                                player_group.update()
                                clock.tick(15)
                            play.rect.y -= 4
                            play.image = load_image('barbarian_1.png')
                            play.y -= 1
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                        else:
                            for i in range(4):
                                play.rect.y -= 4
                                play.image = load_image('barbarian_1_walk_00' + str(i +1) + 'R.png')
                                tiles_group.draw(screen)
                                player_group.draw(screen)
                                pygame.display.flip()
                                player_group.update()
                                clock.tick(15)
                            play.rect.y -= 4
                            play.image = load_image('barbarian_1R.png')
                            play.y -= 1
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                            
                if event.key == pygame.K_DOWN and level[play.y + 1][play.x] in '.Tt#&@=o':
                    if level[play.y + 1][play.x] == '&' and key.intro_text == ['x 1']:
                        if sol == 1:
                            for i in range(4):
                                play.rect.y += 4
                                play.image = load_image('barbarian_1_walk_00' + str(i +1) + '.png')
                                tiles_group.draw(screen)
                                player_group.draw(screen)
                                pygame.display.flip()
                                player_group.update()
                                clock.tick(15)
                            play.rect.y += 4
                            play.image = load_image('barbarian_1.png')
                            play.y += 1
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                        else:
                            for i in range(4):
                                play.rect.y += 4
                                play.image = load_image('barbarian_1_walk_00' + str(i +1) + 'R.png')
                                tiles_group.draw(screen)
                                player_group.draw(screen)
                                pygame.display.flip()
                                player_group.update()
                                clock.tick(15)
                            play.rect.y += 4
                            play.image = load_image('barbarian_1R.png')
                            play.y += 1
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                    elif level[play.y + 1][play.x] != '&':
                        if sol == 1:
                            for i in range(4):
                                play.rect.y += 4
                                play.image = load_image('barbarian_1_walk_00' + str(i +1) + '.png')
                                tiles_group.draw(screen)
                                player_group.draw(screen)
                                pygame.display.flip()
                                player_group.update()
                                clock.tick(15)
                            play.rect.y += 4
                            play.image = load_image('barbarian_1.png')
                            play.y += 1
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                        else:
                            for i in range(4):
                                play.rect.y += 4
                                play.image = load_image('barbarian_1_walk_00' + str(i +1) + 'R.png')
                                tiles_group.draw(screen)
                                player_group.draw(screen)
                                pygame.display.flip()
                                player_group.update()
                                clock.tick(15)
                            play.rect.y += 4
                            play.image = load_image('barbarian_1R.png')
                            play.y += 1
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                if event.key == pygame.K_LEFT and level[play.y][play.x - 1] in '.Tt#&@=o':
                    if level[play.y][play.x - 1] == '&' and key.intro_text == ['x 1']:
                        for i in range(4):
                            play.rect.x -= 4
                            play.image = load_image('barbarian_1_walk_00' + str(i +1) + 'R.png')
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                            clock.tick(15)
                        play.rect.x -= 4
                        play.image = load_image('barbarian_1R.png')
                        play.x -= 1
                        sol = -1
                        tiles_group.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        player_group.update()
                    elif level[play.y][play.x - 1] != '&':
                        for i in range(4):
                            play.rect.x -= 4
                            play.image = load_image('barbarian_1_walk_00' + str(i +1) + 'R.png')
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                            clock.tick(15)
                        play.rect.x -= 4
                        play.image = load_image('barbarian_1R.png')
                        play.x -= 1
                        sol = -1
                        tiles_group.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        player_group.update()
                if event.key == pygame.K_RIGHT and level[play.y][play.x + 1] in '.Tt#&@o=':
                    if level[play.y][play.x + 1] == '&' and key.intro_text != ['x 1']:
                        for i in range(4):
                            play.rect.x += 4
                            play.image = load_image('barbarian_1_walk_00' + str(i +1) + '.png')
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                            clock.tick(15)
                        play.rect.x += 4
                        play.image = load_image('barbarian_1.png')
                        play.x += 1
                        sol = 1
                        tiles_group.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        player_group.update()
                    elif level[play.y][play.x + 1] != '&':
                        for i in range(4):
                            play.rect.x += 4
                            play.image = load_image('barbarian_1_walk_00' + str(i +1) + '.png')
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                            clock.tick(15)
                        play.rect.x += 4
                        play.image = load_image('barbarian_1.png')
                        play.x += 1
                        sol = 1
                        tiles_group.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        player_group.update()
                if event.key == pygame.K_a:
                    if sol == 1:
                        for i in range(3):
                            play.image = load_image('barbarian_1_attack_00' + str(i + 1) + '.png')
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                            clock.tick(15)
                        play.image = load_image('barbarian_1.png')
                        tiles_group.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        player_group.update()
                    else:
                        for i in range(3):
                            play.image = load_image('barbarian_1_attack_00' + str(i + 1) + 'R.png')
                            tiles_group.draw(screen)
                            player_group.draw(screen)
                            pygame.display.flip()
                            player_group.update()
                            clock.tick(15)
                        play.image = load_image('barbarian_1R.png')
                        tiles_group.draw(screen)
                        player_group.draw(screen)
                        pygame.display.flip()
                        player_group.update()
    else:
        for i in range(5):
            play.image = load_image('barbarian_1_die_00' + str(i + 1) + '.png')
            tiles_group.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
            player_group.update()
            clock.tick(15)
        break
    
    clock.tick(15)
    tiles_group.draw(screen)
    for line in key.intro_text:
            string_rendered = key.font.render(line, 9, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            key.text_coord = 40
            intro_rect.top = 45
            intro_rect.x = 55
            screen.blit(string_rendered, intro_rect)
    player_group.draw(screen)
    pygame.display.flip()
    player_group.update()

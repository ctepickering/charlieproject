from typing import Any
import pygame
from pygame.locals import *
import math

pygame.init()
# Screen setup
screen_x =650
screen_y = 650
size = (screen_x, screen_y)
clock = pygame.time.Clock()
level= 1


screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tiny Robot")

# Colours
WHITE = ((255,255,255))
BLUE = ((0,0,255))
GREEN = ((0,255,0))
RED = ((255,0,0))
BLACK = ((0,0,0))
ORANGE = ((255,100,10))
YELLOW = ((255,255,0))


b_image = pygame.image.load('Background.png')
background = pygame.transform.scale(b_image, (screen_x, screen_y))


class Player(pygame.sprite.Sprite):
    # -- Methods
    def __init__(self,x,y):
        self.imgR = pygame.image.load('playerR.png')
        self.imgL= pygame.image.load('playerL.png')
        self.image = pygame.transform.scale(self.imgR, (20, 25)) #scale player size
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y= y
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.jumped = False
        self.vel_y = 0
    #end func

    def update(self):
        # draw player # 
        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 1)

        # player movement #

        change_x = 0
        change_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            change_x -= 2.75
            self.image = pygame.transform.scale(self.imgL, (20, 25))
        #end if
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            change_x += 2.5
            pygame.image.load('playerR.png')
            self.image = pygame.transform.scale(self.imgR, (20, 25)) #scale player size
        # end if  

        if (keys[pygame.K_UP] or keys[pygame.K_w] ) and self.jumped == False:
            self.vel_y = -10
            self.jumped = True

        if pygame.sprite.spritecollide(self, enemy_group, False):
            self.rect.x = self.startx
            self.rect.y = self.starty

        # calculate gravity #

        self.vel_y+= 0.5
        if self.vel_y >10:
            self.vel_y =10
        #end if
        change_y += self.vel_y

        # check for collisions #
        if level == 1 :
            world = level1

        for tile in world.tile_list :
            # check for collision in x #
            if tile[1].colliderect(self.rect.x +change_x, self.rect.y, self.width, self.height) :
                change_x = 0
            # check for collision in y #
            if tile[1].colliderect(self.rect.x, self.rect.y + change_y, self.width, self.height) :
                # check if bellow the ground #
                if self.vel_y < 0 :
                    change_y = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0 :
                    change_y = tile[1].top - self.rect.bottom
                    self.jumped = False
        # update player co ords #
        self.rect.x += change_x
        self.rect.y += change_y

        if self.rect.bottom > screen_y :
            self.rect.bottom = screen_y 
            change_y = 0
        #end if

tile_size = 25
class World():
    def __init__(self,data) -> None:
        self.tile_list = []
        block_img = pygame.image.load('block.png')
        row_pos = 0
        for row in data :
            column_pos = 0
            for tile in row :
                if tile == 1 : # the tile is a block #
                    img = pygame.transform.scale(block_img, (tile_size, tile_size)) #scale block image to size of block
                    img_rect = img.get_rect()
                    img_rect.x = column_pos * tile_size
                    img_rect.y = row_pos * tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile)
                if tile == 4 : # check if it is lava #
                    lava = Lava(column_pos * tile_size,row_pos * tile_size)
                    enemy_group.add(lava)
                column_pos = column_pos +1
            row_pos =row_pos +1
    def draw(self) :
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
        # next tile
    #end procedure

class Lava(pygame.sprite.Sprite):
    def __init__(self,startx,starty):
        super().__init__()
        self.width = 25
        self.height = 25
        self.img= pygame.image.load('acid.png')
        self.image = pygame.transform.scale(self.img, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty
    # end constructor

    def update(self):
            screen.blit(self.image,self.rect)
    # end function

class Obstacle_type1(pygame.sprite.Sprite):
    def __init__(self,startx,starty,direction):
        self.width = 20
        self.height = 20
        self.img= pygame.image.load('movingspike.png')
        self.image = pygame.transform.scale(self.img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty
        self.anchor_pos = startx
        self.step = 0
        self.direction = direction
    #end constructor
    def update(self):
            screen.blit(self.image,self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 1)
            if self.direction == 'p' :
                self.step += 0.02
            else :
                self.step -= 0.02
            self.rect.x =  self. anchor_pos +200* math.sin(self.step)
    #end function
#end class


level1_map= [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1],
[1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1],
[1,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,1,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,1],
[1,0,0,1,1,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

enemy_group = pygame.sprite.Group()
player1 = Player(30, 605)
level1= World(level1_map)

enemy1 = Obstacle_type1(280, 178,'p')
enemy3 = Obstacle_type1(305, 303,'p')
enemy2 = Obstacle_type1(305, 303,'n')

spike_list = pygame.sprite.Group()

spike_list

done= False
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    
    # --- Game logic should go here
    clock.tick(60)
    screen.blit(background, (0,0))
    level1.draw()
    player1.update()
    enemy1.update()
    enemy2.update()
    enemy3.update()
    enemy_group.update()
    pygame.display.update()
    
#endwhile
pygame.quit()
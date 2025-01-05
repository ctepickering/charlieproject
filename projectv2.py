from typing import Any
import pygame
from pygame.locals import *
import math

pygame.init()

clock = pygame.time.Clock()

level = 1

# Screen setup #

screen_x = 650
screen_y = 650
size = (screen_x, screen_y)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tiny Robot")

# Colours #

WHITE = ((255,255,255))
BLUE = ((0,0,255))
GREEN = ((0,255,0))
RED = ((255,0,0))
BLACK = ((0,0,0))
ORANGE = ((255,100,10))
YELLOW = ((255,255,0))

# Classes #

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.Surface([20,25])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y= y
        self.startx = x
        self.starty = y
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.vel_y = 0
        self.isJumped = False
    #end func

    def update(self):
        
        # draw player # 

        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 1)

        # player movement #

        change_x = 0
        change_y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            change_x -= 3
        #end if
        if keys[pygame.K_RIGHT]:
            change_x += 3
        # end if  
        if keys[pygame.K_UP] and self.isJumped == False:
            self.vel_y = -10
            self.isJumped=True
        #end if

        # calculate gravity #

        self.vel_y+= 0.5
        if self.vel_y >10:
            self.vel_y =10
        #end if

        change_y +=self.vel_y

        # check player collision #

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
                    self.isJumped=False

        # collision with enemies # 
        if pygame.sprite.spritecollide(self, spike_group, False):
            self.rect.x = self.startx
            self.rect.y = self.starty

        # update player coordinates #

        self.rect.x += change_x
        self.rect.y += change_y

        if self.rect.bottom > screen_y :
            self.rect.bottom = screen_y 
            change_y = 0
        #end if

class Enemy_type1(pygame.sprite.Sprite):
    def __init__(self,startx,starty,direction):
        super().__init__()
        self.width = 20
        self.height = 20
        self.image = pygame.Surface([20,20])
        self.image.fill(ORANGE)
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


tile_size = 25
class World():
    def __init__(self,data) -> None:
        self.tile_list = []
        row_pos = 0
        for row in data :
            column_pos = 0
            for tile in row :
                if tile == 1 : # the tile is a block #
                    img = pygame.Surface([tile_size,tile_size])
                    img.fill(GREEN)
                    img_rect = img.get_rect()
                    img_rect.x = column_pos * tile_size
                    img_rect.y = row_pos * tile_size
                    tile = (img,img_rect)
                    self.tile_list.append(tile)
                if tile == 2 : # check if tile is enemy p direction #
                    spike = Enemy_type1(column_pos * tile_size,row_pos * tile_size, 'p')
                    spike_group.add(spike)
                if tile == 3 : # check if tile is enemy n direction #
                    spike = Enemy_type1(column_pos * tile_size,row_pos * tile_size, 'n')
                    spike_group.add(spike)
                column_pos = column_pos +1
            row_pos =row_pos +1

    #end func
    def draw(self) :
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            pygame.draw.rect(screen, WHITE, tile[1], 1)
    #end func


level1_map= [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
[1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1],
[1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,1,0,0,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,2,3,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1],
[1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,1,1,1],
[1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
[1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

# Objects #

player1 = Player(30, 600)

spike_group = pygame.sprite.Group()

level1= World(level1_map)


# Main Program Loop #

done= False
while not done:

    # Main event loop #

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    
    # Game logic #

    clock.tick(60)
    screen.fill(BLACK)
    level1.draw()
    spike_group.update()
    player1.update()

    pygame.display.update()
    
#endwhile
pygame.quit()
from typing import Any
import pygame
from pygame.locals import *
import math
import random

pygame.init()

clock = pygame.time.Clock()

# Screen setup #

screen_x = 650
screen_y = 650
size = (screen_x, screen_y)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tiny Robot")

level = 1

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
        self.levelDone = False
    #end func

    def update(self):

        self.level =1

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

        
        world =  current_level

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
        if pygame.sprite.spritecollide(self, enemy_group, False):
            self.rect.x = self.startx
            self.rect.y = self.starty

        # collision with checkpoint # 
        if pygame.sprite.spritecollide(self, checkpoint_group, False):
            self.levelDone = True

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
        self.image = pygame.Surface([self.width,self.height])
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

class Lava(pygame.sprite.Sprite):
    def __init__(self,startx,starty):
        super().__init__()
        self.width = 25
        self.height = 25
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty
    # end constructor

    def update(self):
            screen.blit(self.image,self.rect)
    # end function

class Enemy_type3(pygame.sprite.Sprite):
    def __init__(self,start_y):
        super().__init__()
        self.image = pygame.Surface([15,30])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(25,screen_x-40)
        self.rect.y= start_y - random.randint(1,100)
        self.start_y = start_y - random.randint(1,100)
        self.vel_y = 0
    # end function

    def update(self):
            screen.blit(self.image,self.rect)

            change_y = 0
            
            # calculate gravity #

            self.vel_y+= 0.5
            if self.vel_y >10:
                self.vel_y =10
            # end if

            change_y +=self.vel_y

            if self.rect.y > screen_y + random.randint(10,1000) :
                self.rect.y = self.start_y
                self.rect.x = random.randint(25,screen_x-40)
                self.vel_y = 0
            # end if 

            self.rect.y += change_y

    # end function

class Level_End(pygame.sprite.Sprite):
    def __init__(self,startx,starty):
        super().__init__()
        self.width = 45
        self.height = 45
        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty
    # end constructor

    def update(self):
            screen.blit(self.image,self.rect)
    # end function



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
                    enemy_group.add(spike)
                if tile == 3 : # check if tile is enemy n direction #
                    spike = Enemy_type1(column_pos * tile_size,row_pos * tile_size, 'n')
                    enemy_group.add(spike)
                if tile == 4 : # check if it is lava #
                    lava = Lava(column_pos * tile_size,row_pos * tile_size)
                    enemy_group.add(lava)
                if tile == 5 : # check if falling debris #
                    debris = Enemy_type3(row_pos * tile_size)
                    enemy_group.add(debris)
                if tile == 6 : # check if tile is level endpoint #
                    checkpoint = Level_End(column_pos * tile_size + 2.5 ,row_pos * tile_size + 2.5 )
                    checkpoint_group.add(checkpoint)
                column_pos = column_pos +1
            row_pos =row_pos +1

    #end func
    def draw(self) :
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
            pygame.draw.rect(screen, WHITE, tile[1], 1)
    #end func


level3_map= [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,1,1,1,1,1,0,0,5,5,5,0,0,0,0,0,0,0,1,1,1],
[1,0,0,0,0,0,6,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
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
[1,0,0,0,0,1,1,1,1,4,4,4,4,4,4,4,4,4,4,4,4,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

level2_map= [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,1,1,1,1,1,0,0,5,5,5,0,0,0,0,0,0,0,1,1,1],
[1,0,0,0,0,0,6,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
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
[1,0,0,0,0,1,1,1,1,4,4,4,4,4,4,4,4,4,4,4,4,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

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

# Objects #

player1 = Player(30, 600)

enemy_group = pygame.sprite.Group()

checkpoint_group = pygame.sprite.Group()

current_level= World(level1_map)

def reset_level():
    player1.rect.x = 30
    player1.rect.y = 600
    enemy_group.empty()
    checkpoint_group.empty()
    


def getlevel():
    if level == 1 :
        current_level= World(level1_map)
    elif level == 2 :
        current_level= World(level2_map)
    return(current_level)





# Main Program Loop #

done= False
while not done:

    # Main event loop #

    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    
    # Game logic #
    if player1.levelDone == True :
        level += 1
        reset_level()
        current_level = getlevel()
        player1.levelDone = False
    #end if
    clock.tick(60)
    screen.fill(BLACK)
    current_level.draw()
    enemy_group.update()
    player1.update()
    checkpoint_group.update()

    pygame.display.update()
    
#endwhile
pygame.quit()
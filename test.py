import pygame
import random

# Initialize the game engine
pygame.init()

# Define some colors
WHITE = ((255,255,255))
BLUE = ((0,0,255))
GREEN = ((0,255,0))
RED = ((255,0,0))
BLACK = ((0,0,0))
ORANGE = ((255,100,10))
YELLOW = ((255,255,0))
BLUE_GREEN = ((0,255,170))
MARROON = ((115,0,0))
LIME = ((180,255,100))
PINK = ((255,100,180))
PURPLE = ((240,0,255))
GREY = ((127,127,127))
MAGENTA = ((255,0,230))
BROWN = ((100,40,0))
FOREST_GREEN = ((0,50,0))
NAVY_BLUE= ((0,0,100))
RUST = ((210,150,75))
DANDILION_YELLOW = ((255,200,0))
HIGHLIGHTER = ((255,255,100))
SKY_BLUE = ((0,255,255))
MOONGLOW = ((235,245,255))

# - - # GLOBAL VARIABLES # - - #

gravity = 1
screen_x =600
screen_y = 500
size = (screen_x, screen_y)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("The Tower")
map =[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

clock = pygame.time.Clock()

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#classes go here


class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 5
        self.height = 5
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE), 
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        self.jump_height= 12
        self.vel_y = 0
        self.move = 0
    

    def update(self):
        keys = pygame.key.get_pressed() # checks for keys getting pressed

        self.vel_y += gravity # causes the player to fall due to gravity if in the air

        self.rect.y += self.vel_y # causes acceleration downwards for the longer the time in the air

        # Check if player is on the ground
        if self.rect.bottom > screen_y:
            self.rect.bottom = screen_y
            self.vel_y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move = -5
            self.rect.x += self.move
        #end if
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.move = 5
            self.rect.x += self.move
        # end if  
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.bottom == screen_y:
                self.vel_y = -self.jump_height
        #end if
        else :
            self.move=0
        wall_collisions = pygame.sprite.spritecollide(self, wall_list, False)
        for wall in wall_collisions:
            if self.move > 0:
                self.rect.right = wall.rect.left
            elif self.move < 0:
                self.rect.left = wall.rect.right
            elif self.rect.bottom > wall.rect.top:
                self.rect.bottom = wall.rect.top
                self.vel_y =0
            #elif self.vel_y < 0:
                #self.rect.top = wall.rect.bottom
#end class
                
class Block(pygame.sprite.Sprite):
    #Define the constructor for block
    def __init__(self,colour,width,height,x_ref,y_ref):
        #Call the sprite constructor
        super().__init__()
        self.width = width
        self.height = height
        #Create a sprite and fill it with colour
        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(colour)
        self.rect=self.image.get_rect()#Set the position of the player attributes
        self.rect.x=x_ref
        self.rect.y=y_ref

        def update(self):
            self=self
            

#create sprite groups
all_sprites = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
for y in range(25):
    for x in range(30):
        if map[y][x]==1:
            wall=Block(BLUE,20,20,(x*20),(y*20))
            wall_list.add(wall)
            all_sprites.add(wall)
plur=player()

all_sprites.add(plur)


 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    
    # --- Game logic should go here

    #check for collisions
    
    #update game objects
    all_sprites.update()
    # --- Drawing code should go here
 
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    
    
    screen.fill(BLACK)
    
    #draw stuff here:
    all_sprites.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
#endwhile
pygame.quit()
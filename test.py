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

clock = pygame.time.Clock()

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
#classes go here

class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 20
        self.height = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE), 
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 480
        self.jump_height= 20
        self.vel_y = 0

    

    def update(self):
        keys = pygame.key.get_pressed() # checks for keys getting pressed

        self.vel_y += gravity # causes the player to fall due to gravity if in the air

        self.rect.y += self.vel_y # causes acceleration downwards for the longer the time in the air

        # Check if player is on the ground
        if self.rect.bottom > screen_y:
            self.rect.bottom = screen_y
            self.vel_y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5
        #end if
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5
        # end if
            
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.bottom == screen_y:
                self.vel_y = -self.jump_height
        #end if
    
#end class
            
       


#global variables
x_val2 = 350
enemy_count = 5
x_val = 0
y_val = 200
x_offset = 1
pi= 3.141592652
counter = 0
end = ""
score = 0

#create sprite groups
all_sprites = pygame.sprite.Group()

plur=player()

all_sprites.add(plur)
#set the enemy count
Invader_Num = enemy_count


 
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
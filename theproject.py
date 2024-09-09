import pygame

# Screen setup
screen_x =650
screen_y = 650
size = (screen_x, screen_y)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("The Tower")

# Colours
WHITE = ((255,255,255))
BLUE = ((0,0,255))
GREEN = ((0,255,0))
RED = ((255,0,0))
BLACK = ((0,0,0))
ORANGE = ((255,100,10))
YELLOW = ((255,255,0))

background = pygame.image.load('Background.png')

done= False
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    
    # --- Game logic should go here

    screen.blit(background, (0,0))

    pygame.display.flip()
    
    #clock.tick(60)
#endwhile
pygame.quit()
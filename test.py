import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.hovered = False
    
    def draw(self, screen):
        # Change color on hover
        current_color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        
        # Render text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and self.action:
                self.action()

# Example usage
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((500, 400))
    pygame.display.set_caption("Button Example")
    
    font = pygame.font.Font(None, 36)
    def on_click():
        print("Button Clicked!")
    
    button = Button(150, 150, 200, 60, "Click Me", font, (0, 128, 255), (0, 200, 255), (255, 255, 255), on_click)
    
    running = True
    while running:
        screen.fill((30, 30, 30))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            button.handle_event(event)
        
        button.draw(screen)
        pygame.display.flip()
    
    pygame.quit()

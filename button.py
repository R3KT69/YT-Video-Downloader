import pygame

class Button:
    def __init__(self, x,y,width,height,color, text="BUTTON"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def Spawn(self):
        print(f"Created")
    
    def GetRect(self):
        return self.Rect
    
    def DrawButton(self, screen, font):
        pygame.draw.rect(screen, self.color, self.Rect)
        text_surface = font.render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.Rect.center)
        screen.blit(text_surface, text_rect)
    
    def IsInside(self, mouseX, mouseY):
        if self.GetRect().collidepoint(mouseX, mouseY):
            print(f"{mouseX, mouseY}: Inside")
            return True
        
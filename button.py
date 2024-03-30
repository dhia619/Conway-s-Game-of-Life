import pygame
from time import sleep
class Button:
    def __init__(self,text,img_path,pos,elevation):
        self.text = text
        #self.text_surface = font.render(self.text,True,(255,255,255))
        if img_path:
            self.image = pygame.image.load(img_path)
        self.pos = pos
        self.elevation = elevation
        
        self.rect = pygame.Rect(pos[0],pos[1],50,30)
        self.on_color = (25,76,160)
        self.off_color = (123, 143, 161)
        self.bottom_rect_color = (207, 185, 151)
        self.bottom_rect = pygame.Rect(self.rect.x,self.rect.y+self.elevation,self.rect.width,self.rect.height)
        self.color = self.off_color
        self.pressed = False
    def draw(self,screen):
        pygame.draw.rect(screen,self.bottom_rect_color,self.bottom_rect,border_radius=8)
        pygame.draw.rect(screen,self.color,self.rect,border_radius=8)
        screen.blit(self.image,(self.rect.centerx-self.image.get_width()//2,self.rect.centery-self.image.get_height()//2))
        #screen.blit(self.text_surface,(self.rect.centerx-self.text_surface.get_width()//2,self.rect.centery-self.text_surface.get_height()//2))
    def update(self):
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.color = self.on_color
            if mouse[0]:
                self.pressed = True
                self.rect.y = self.bottom_rect.y
                sleep(0.1)
            else:
                self.rect.y = self.bottom_rect.y-self.elevation
                self.pressed = False
        else:
            self.rect.y = self.bottom_rect.y-self.elevation
            self.color = self.off_color
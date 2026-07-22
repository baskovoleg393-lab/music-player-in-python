from colors import colors
import pygame as pg
from time import sleep
import keyboard as key

class Root:
    def __init__(self, main = lambda:None, size = (500, 500), background = colors.black, fps = 60):
        self.main = main
        self.size = size
        self.background = background
        self.flag = True
        self.time = 0
        self.clock = pg.time.Clock()
        self.fps = fps
        self.events = []

    def Start(self):
        self.screen = pg.display.set_mode(self.size, pg.NOFRAME)
        while self.flag:
            self.events = pg.event.get()

            try:
                self.main()
            except Exception as e:
                return e

            pg.display.flip()
            self.screen.fill(self.background())
            self.clock.tick(self.fps)

        pg.quit()
        return None

class Key:
    def __init__(self, key_name):
        self.name = key_name
        self.up = False
        self.down = False
        self.press = False
        self.old_press = False

    def update(self):
        self.press = key.is_pressed(self.name)

        self.up = not self.press and self.old_press
        self.down = self.press and not self.old_press

        self.old_press = self.press

class Button:
    def __init__(self, x, y, w, h, text, color=(100, 100, 100), hover_color=(150, 150, 150)):
        self.rect = pg.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hover = False
    
    def draw(self, screen):
        color = self.hover_color if self.is_hover else self.color
        pg.draw.rect(screen, color, self.rect, border_radius=5)
        font = pg.font.Font(None, 20)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
    
    def handle_event(self, event):
        if event.type == pg.MOUSEMOTION:
            self.is_hover = self.rect.collidepoint(event.pos)
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


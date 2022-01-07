import pygame


class CheckButton:
    def __init__(self, w, h, x, y):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.def_image = None
        self.check_image = None
        self.image = self.def_image
        self.checked = False

    def get_event(self):
        mouse = pygame.mouse.get_pos()
        if (self.x < mouse[0] < self.x + self.w) and (self.y < mouse[1] < self.y + self.h):
            self.checked = not self.checked
            return ['clicked']
        return []

    def update(self):
        if self.checked:
            self.image = self.check_image
        else:
            self.image = self.def_image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

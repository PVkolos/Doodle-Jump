import pygame


class Button:
    def __init__(self, w, h, x, y):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.def_image = None
        self.image = self.def_image
        self.func = self.do_nothing

    def do_nothing(self):
        pass

    def connect(self, func):
        self.func = func

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class CheckButton(Button):
    def __init__(self, w, h, x, y):
        super().__init__(w, h, x, y)
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.def_image = None
        self.check_image = None
        self.image = self.def_image
        self.checked = False
        self.func = self.do_nothing

    def connect(self, func):
        self.func = func

    def update(self):
        mouse = pygame.mouse.get_pos()
        if (self.x < mouse[0] < self.x + self.w) and (self.y < mouse[1] < self.y + self.h):
            self.checked = not self.checked
            self.func()
        if self.checked:
            self.image = self.check_image
        else:
            self.image = self.def_image


class PushButton(Button):
    def __init__(self, w, h, x, y):
        super().__init__(w, h, x, y)

    def update(self):
        mouse = pygame.mouse.get_pos()
        if (self.x < mouse[0] < self.x + self.w) and (self.y < mouse[1] < self.y + self.h):
            self.func()

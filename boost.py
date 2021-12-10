import pygame


class Boost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 80


class StaticBoost(Boost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("images/green.png").convert_alpha()
        self.sound = pygame.mixer.Sound('sfx/jump.wav')

    def play_sound(self):
        self.sound.play()


class RedBoost(Boost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load("images/red.png").convert_alpha()
        self.is_destroyed = False
        self.sound = pygame.mixer.Sound('sfx/break.mp3')

    def play_sound(self):
        if self.is_destroyed:
            pass
        else:
            self.sound.play()
            self.is_destroyed = True


class FederBoost(Boost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sound = pygame.mixer.Sound('sfx/jump.wav')
        self.feder_sound = pygame.mixer.Sound('sfx/feder.mp3')
        self.is_feder = False

    def play_sound(self):
        if self.is_feder:
            self.feder_sound.play()
        else:
            self.sound.play()


class MovementBoost(Boost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sound = pygame.mixer.Sound('sfx/jump.wav')

    def play_sound(self):
        self.sound.play()

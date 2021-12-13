import pygame


class Boost(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.size = 80


class StaticBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = pygame.image.load("images/green.png").convert_alpha()
        self.sound = pygame.mixer.Sound('sfx/jump.wav')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def play_sound(self):
        self.sound.play()


class RedBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = pygame.image.load("images/red.png").convert_alpha()
        self.is_destroyed = False
        self.sound = pygame.mixer.Sound('sfx/break.mp3')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def play_sound(self):
        if self.is_destroyed:
            pass
        else:
            self.sound.play()
            self.is_destroyed = True


class FederBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.sound = pygame.mixer.Sound('sfx/jump.wav')
        self.feder_sound = pygame.mixer.Sound('sfx/feder.mp3')
        self.is_feder = False
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def play_sound(self):
        if self.is_feder:
            self.feder_sound.play()
        else:
            self.sound.play()


class MovementBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = pygame.image.load("images/blue.png").convert_alpha()
        self.sound = pygame.mixer.Sound('sfx/jump.wav')
        self.right = True
        self.left = True
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def play_sound(self):
        self.sound.play()

    def update(self):
        if self.x < 55:
            self.left = False
            self.right = True
            self.x += 5
        elif self.x >= 500:
            self.left = True
            self.right = False
        if self.left:
            self.x -= 5
        else:
            self.x += 5


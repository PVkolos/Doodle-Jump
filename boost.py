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
        self.image = pygame.image.load("images/green.png").convert_alpha()
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

    def get_image(self):
        if self.is_feder:
            self.image_spring = pygame.image.load("images/spring2.png").convert_alpha()
        else:
            self.image_spring = pygame.image.load("images/spring_comp.png").convert_alpha()
        return self.image_spring


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


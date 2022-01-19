import pygame
from file_manager import get_image, get_sound


class Boost(pygame.sprite.Sprite):
    def __init__(self, x: int = 0, y: int = 0, *groups):
        super().__init__(*groups)
        self.size = 80
        self.image = pygame.image.load(get_image('static_b.png')).convert_alpha()
        self.sound = pygame.mixer.Sound(get_sound('jump.wav'))
        self.jump_range = 200
        self.jump_speed = 5
        self.rect = pygame.rect.Rect(0, 0, 114, 10)
        self.rect.x = x
        self.rect.y = y

    def update(self, screen: pygame.Surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def play_sound(self):
        self.sound.play()

    def jump(self):
        pass


class StaticBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)


class RedBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = pygame.image.load(get_image('red_b.png')).convert_alpha()
        self.destroy_image = pygame.image.load(get_image('red3_b.png')).convert_alpha()
        self.is_destroyed = False
        self.sound = pygame.mixer.Sound(get_sound('break.mp3'))
        self.fall_speed = 5
        self.jump_range = 0
        self.jump_speed = 0

    def play_sound(self):
        if not self.is_destroyed:
            self.sound.play()

    def update(self, screen: pygame.Surface):
        if self.is_destroyed:
            self.rect.y += self.fall_speed
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def jump(self):
        self.is_destroyed = True
        self.image = self.destroy_image


class FederBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.sound = pygame.mixer.Sound(get_sound('jump.wav'))
        self.feder_sound = pygame.mixer.Sound(get_sound('feder.mp3'))
        self.spring_image = pygame.image.load(get_image('spring_comp.png')).convert_alpha()
        self.spring_image2 = pygame.image.load(get_image('spring2.png')).convert_alpha()
        self.is_feder = False
        self.jump_range = 1000
        self.jump_speed = 10

    def play_sound(self):
        self.feder_sound.play()

    def get_image(self) -> pygame.Surface:
        image_spring = self.spring_image
        if self.is_feder:
            image_spring = self.spring_image2
        return image_spring

    def update(self, screen: pygame.Surface):
        screen.blit(self.get_image(), (self.rect.x + 30, self.rect.y - 35))
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def jump(self):
        self.is_feder = True


class MovementBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = pygame.image.load(get_image('move_b.png')).convert_alpha()
        self.sound = pygame.mixer.Sound(get_sound('jump.wav'))
        self.speed = 5
        self.direction = 1

    def update(self, screen: pygame.Surface):
        if self.rect.x < 55 or self.rect.x >= 520:
            self.direction = -self.direction
        self.rect.x += self.direction * self.speed
        screen.blit(self.image, (self.rect.x, self.rect.y))

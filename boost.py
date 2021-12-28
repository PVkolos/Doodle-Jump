import pygame
from image_manager import get_image


class Boost(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.size = 80
        self.image = pygame.image.load(get_image('static_b.png')).convert_alpha()
        self.sound = pygame.mixer.Sound('sfx/jump.wav')
        self.jump_range = 200
        self.jump_speed = 5

    def update(self) -> None:
        pass

    def play_sound(self):
        self.sound.play()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x - 60 / 2, self.y))

    def jump(self):
        pass


class StaticBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class RedBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = pygame.image.load(get_image('red_b.png')).convert_alpha()
        self.destroy_image = pygame.image.load(get_image('red3_b.png')).convert_alpha()
        self.is_destroyed = False
        self.sound = pygame.mixer.Sound('sfx/break.mp3')
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.fall_speed = 5
        self.jump_range = 0
        self.jump_speed = 0

    def play_sound(self):
        if not self.is_destroyed:
            self.sound.play()

    def update(self) -> None:
        if self.is_destroyed:
            self.y += self.fall_speed

    def jump(self):
        self.is_destroyed = True
        self.image = self.destroy_image


class FederBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.sound = pygame.mixer.Sound('sfx/jump.wav')
        self.feder_sound = pygame.mixer.Sound('sfx/feder.mp3')
        self.spring_image = pygame.image.load("images/spring_comp.png").convert_alpha()
        self.spring_image2 = pygame.image.load("images/spring2.png").convert_alpha()
        self.is_feder = False
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.jump_range = 1000
        self.jump_speed = 10

    def play_sound(self):
        self.feder_sound.play()

    def get_image(self) -> pygame.Surface:
        image_spring = self.spring_image
        if self.is_feder:
            image_spring = self.spring_image2
        return image_spring

    def draw(self, screen: pygame.Surface):
        screen.blit(self.get_image(), (self.x - 60 / 2 + 30, self.y - 35))
        screen.blit(self.image, (self.x - 60 / 2, self.y))

    def jump(self):
        self.is_feder = True


class MovementBoost(Boost):
    def __init__(self, x, y, *groups):
        super().__init__(x, y, *groups)
        self.image = pygame.image.load(get_image('move_b.png')).convert_alpha()
        self.sound = pygame.mixer.Sound('sfx/jump.wav')
        self.right = True
        self.left = True
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self) -> None:
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

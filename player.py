import pygame
from image_manager import get_image


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, *groups):
        super().__init__(*groups)
        self.width = 60
        self.pl_right = pygame.image.load(get_image('right_1.png')).convert_alpha()
        self.pl_left = pygame.image.load(get_image('left_1.png')).convert_alpha()
        self.pl_left_pr = pygame.image.load(get_image('left.png')).convert_alpha()
        self.pl_right_pr = pygame.image.load(get_image('right.png')).convert_alpha()
        self.image = self.pl_right
        self.is_jump = False
        self.screen = screen
        self.jump = 0
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.y = 400
        self.rect.x = 270
        self.speed_down = 5
        self.speed_up = 5
        self.shoot_pass = 0

    def down(self, boosts, monsters):
        for el in boosts:
            if ((el.x - 40 <= self.rect.x <= el.x + 55) or (el.x - 40 <= self.rect.x + self.width <= el.x + 55)) and self.rect.y == \
                    el.y and not self.is_jump:
                self.is_jump = True
                self.jump = el.jump_range
                self.speed_up = el.jump_speed
                el.play_sound()
                el.jump()
        if not self.is_jump:
            self.rect.y += self.speed_down
        elif self.jump == 0 or self.jump < 0:
            self.is_jump = False
            self.speed_up = 5
        elif self.is_jump:
            if self.rect.y <= 400:
                for el in boosts:
                    el.y += self.speed_up
                for monster in monsters:
                    monster.rect.y += self.speed_up
                self.rect.y += self.speed_up
            self.rect.y -= self.speed_up
            self.jump -= self.speed_up
            if self.image == self.pl_right and self.jump > 100:
                self.image = self.pl_right_pr
            elif self.image == self.pl_left and self.jump > 100:
                self.image = self.pl_left_pr
            elif self.jump <= 100 and self.image == self.pl_right_pr:
                self.image = self.pl_right
            elif self.jump <= 100 and self.image == self.pl_left_pr:
                self.image = self.pl_left
        self.screen.blit(self.image, (self.rect.x, self.rect.y - 82))

    def shoot(self):
        self.shoot_pass = 60
        return Bullet(self.rect.x, self.rect.y - 82)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.rect.x, self.rect.y - 82))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.speed = 10
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.sound = pygame.mixer.Sound('sfx/pistol_shoot.mp3')
        self.play_sound()

    def play_sound(self):
        self.sound.play()

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.image_one = pygame.image.load("images/bat1.png").convert_alpha()
        self.image_two = pygame.image.load("images/bat2.png").convert_alpha()
        self.image_free = pygame.image.load("images/bat3.png").convert_alpha()
        self.im_dict = {0: self.image_one, 1: self.image_two, 2: self.image_free}
        self.image = self.im_dict[0]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.right = True
        self.left = True
        self.rect.x = x
        self.rect.y = y
        self.i = 1

    def update(self):
        self.image = self.im_dict[self.i % 3]
        if self.rect.x < 55:
            self.left = False
            self.right = True
            self.rect.x += 5
        elif self.rect.x >= 500:
            self.left = True
            self.right = False
        if self.left:
            self.rect.x -= 5
        else:
            self.rect.x += 5
        self.i += 1

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))

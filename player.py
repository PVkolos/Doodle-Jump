import pygame
from boost import StaticBoost, RedBoost, MovementBoost, FederBoost


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, *groups):
        super().__init__(*groups)
        self.y = 400
        self.x = 270
        self.width = 60
        self.pl_right = pygame.image.load("images/right_1.png").convert_alpha()
        self.pl_left = pygame.image.load("images/left_1.png").convert_alpha()
        self.pl_left_pr = pygame.image.load("images/left.png").convert_alpha()
        self.pl_right_pr = pygame.image.load("images/right.png").convert_alpha()
        self.image = self.pl_right
        self.jump = False
        self.screen = screen
        self.is_jump = 0
        self.rect = self.image.get_rect()
        self.speed_down = 5
        self.speed_up = 5

    def down(self, boosts):
        for el in boosts:
            if ((el.x - 40 <= self.x <= el.x + 55) or (el.x - 40 <= self.x + self.width <= el.x + 55)) and self.y == \
                    el.y and not self.jump:
                if type(el) == StaticBoost or type(el) == MovementBoost:
                    self.jump = True
                    self.is_jump = 200
                elif type(el) == FederBoost:
                    el.is_feder = True
                    self.jump = True
                    self.is_jump = 1000
                    self.speed_up = 10
                else:
                    el.image = pygame.image.load("images/red_1.png").convert_alpha()
                el.play_sound()
        if not self.jump:
            self.y += self.speed_down
        elif self.is_jump == 0 or self.is_jump < 0:
            self.jump = False
            self.speed_up = 5
        elif self.jump:
            if self.y <= 400:
                for el in boosts:
                    el.y += self.speed_up
                self.y += self.speed_up
            self.y -= self.speed_up
            self.is_jump -= self.speed_up
            if self.image == self.pl_right and self.is_jump > 100:
                self.image = self.pl_right_pr
            elif self.image == self.pl_left and self.is_jump > 100:
                self.image = self.pl_left_pr
            elif self.is_jump <= 100 and self.image == self.pl_right_pr:
                self.image = self.pl_right
            elif self.is_jump <= 100 and self.image == self.pl_left_pr:
                self.image = self.pl_left
        self.screen.blit(self.image, (self.x, self.y - 82))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pass

    def update(self):
        pass

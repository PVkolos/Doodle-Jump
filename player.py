import pygame
from boost import StaticBoost, RedBoost, MovementBoost


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

    def down(self, boosts):
        for el in boosts:
            if ((el.x - 40 <= self.x <= el.x + 55) or (el.x - 40 <= self.x + self.width <= el.x + 55)) and self.y == \
                    el.y and not self.jump:
                if type(el) == StaticBoost or type(el) == MovementBoost:
                    self.jump = True
                    self.is_jump = 200
                else:
                    el.image = pygame.image.load("images/red_1.png").convert_alpha()
                el.play_sound()
        if not self.jump:
            self.y += 5
        elif self.is_jump == 0 or self.is_jump < 0:
            self.jump = False
        elif self.jump:
            if self.y <= 400:
                for el in boosts:
                    el.y += 5
                self.y += 5
            self.y -= 5
            self.is_jump -= 5
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

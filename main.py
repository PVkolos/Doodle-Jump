import pygame
import random


class Player:
    def __init__(self, screen):
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

    def down(self, boosts):
        for el in boosts:
            if ((el.x - 40 <= self.x <= el.x + 55) or (el.x - 40 <= self.x + self.width <= el.x + 55)) and self.y == \
                    el.y and not self.jump:
                self.jump = True
                self.is_jump = 200
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


class Boost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 80


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 800))
        self.screen.set_alpha(None)
        self.bg = pygame.image.load("images/bg.jpg")
        self.boosts = [Boost(100, 750), Boost(300, 750), Boost(500, 750)]
        self.pl = Player(self.screen)
        self.clock = pygame.time.Clock()
        self.image_boost = pygame.image.load("images/green.png").convert_alpha()
        self.flag = True
        self.score = 0
        self.running = True
        pygame.display.set_caption('DoodleJumpDemo')

    def draw(self, boosts):
        for boost in boosts:
            self.screen.blit(self.image_boost, (boost.x - 60 / 2, boost.y))

    def check_play(self):
        if len(self.boosts) < 15:
            for i in range(15 - len(self.boosts)):
                coord = (random.randint(80, 600 - 80),
                         random.randrange(round(self.boosts[-1].y - 150), round(self.boosts[-1].y), 5))
                self.boosts.append(Boost(coord[0], coord[1]))
        if self.pl.x < -80:
            self.pl.x = 580
        elif self.pl.x > 680:
            self.pl.x = -40
        a = self.boosts.copy()
        for i in range(len(a)):
            if a[i].y > 800:
                del self.boosts[i]
                self.score += 100

    def get_fps(self):
        f2 = pygame.font.SysFont('serif', 14)
        text2 = f2.render(f'FPS: {int(self.clock.get_fps() // 1)}', False,
                          (255, 0, 0))

        self.screen.blit(text2, (10, 10))

    def game_over(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        app = App()
                        app.start()
            self.screen.fill((0, 0, 0))
            f2 = pygame.font.SysFont('serif', 20)
            text2 = f2.render('press "space" to play', False,
                              (255, 0, 0))
            f3 = pygame.font.SysFont('serif', 30)
            text3 = f3.render('game over', False,
                              (255, 0, 0))
            self.screen.blit(text3, (230, 250))
            self.screen.blit(text2, (200, 350))
            pygame.display.flip()

    def set_score(self):
        if self.score < 0:
            f2 = pygame.font.SysFont('serif', 20)
            text2 = f2.render(str(self.score - 500), False,
                              (255, 0, 0))
            self.screen.blit(text2, (560, 10))
        elif self.score == 0:
            f2 = pygame.font.SysFont('serif', 20)
            text2 = f2.render(str(self.score), False,
                              (255, 0, 0))
            self.screen.blit(text2, (560, 10))
        else:
            f2 = pygame.font.SysFont('serif', 20)
            text2 = f2.render(str(self.score - 400), False,
                              (255, 0, 0))
            self.screen.blit(text2, (560, 10))

    def functions(self):
        self.clock.tick(60)
        self.check_play()
        self.screen.blit(self.bg, (0, 0))
        self.draw(self.boosts)
        self.pl.down(self.boosts)
        self.get_fps()
        self.set_score()

    def start(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.pl.image = self.pl.pl_left
                self.pl.x -= 3
            if keys[pygame.K_RIGHT]:
                self.pl.image = self.pl.pl_right
                self.pl.x += 3
            self.functions()
            if self.pl.y > 800:
                self.flag = False
                break
            pygame.display.flip()

        if not self.flag:
            self.running = True
            self.game_over()
        else:
            pygame.quit()


if __name__ == '__main__':
    app = App()
    app.start()

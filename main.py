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
        self.jump_sound = pygame.mixer.Sound('sfx/jump.wav')
        self.platform_destroy_sound = pygame.mixer.Sound('sfx/break.mp3')
        self.image = self.pl_right
        self.jump = False
        self.screen = screen
        self.is_jump = 0

    def down(self, boosts):
        for el in boosts:
            if ((el.x - 40 <= self.x <= el.x + 55) or (el.x - 40 <= self.x + self.width <= el.x + 55)) and self.y == \
                    el.y and not self.jump:
                if el.static:
                    self.jump = True
                    self.is_jump = 200
                    self.jump_sound.play()
                else:
                    el.image = pygame.image.load("images/red_1.png").convert_alpha()
                    self.platform_destroy_sound.play()
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
    def __init__(self, x, y, static=True):
        self.x = x
        self.y = y
        self.size = 80
        self.image = None
        self.static = static
        if self.static:
            self.image = pygame.image.load("images/green.png").convert_alpha()
        else:
            self.image = pygame.image.load("images/red.png").convert_alpha()


class App:
    def __init__(self):
        pygame.init()
        self.pause_flag = False
        self.screen = pygame.display.set_mode((600, 800))
        self.screen.set_alpha(None)
        self.lose_sound = pygame.mixer.Sound('sfx/pada.mp3')
        self.bg = pygame.image.load("images/bg.jpg")
        self.start_screen = pygame.image.load("images/start_screen_bg.jpg")
        self.game_over_bg = pygame.image.load("images/game_over_bg.jpg")
        self.boosts = [Boost(100, 750, True), Boost(300, 750, True), Boost(500, 750, True)]
        self.pl = Player(self.screen)
        self.clock = pygame.time.Clock()
        self.flag = True
        self.score = 0
        self.cc = 0
        self.running = True
        self.cntr = 0

        pygame.display.set_caption('DoodleJumpDemo')

    def draw(self, boosts):
        for boost in boosts:
            self.screen.blit(boost.image, (boost.x - 60 / 2, boost.y))

    def check_play(self):
        if len(self.boosts) < 15:
            for _ in range(15 - len(self.boosts)):
                y = self.boosts[-1].y
                if not self.boosts[-1].static:
                    for i in range(2, 15):
                        if self.boosts[-i].static:
                            y = self.boosts[-i].y
                            break
                coord = (random.randint(80, 600 - 80),
                         random.randrange(round(y - 150), round(y), 5))
                if random.choice([1, 1, 0, 1, 1, 1]) == 1:
                    static = True
                else:
                    static = False
                self.boosts.append(Boost(coord[0], coord[1], static))
        if self.pl.x < -80:
            self.pl.x = 580
        elif self.pl.x > 680:
            self.pl.x = -40
        a = self.boosts.copy()
        for i in range(len(a)):
            if a[i].y > 800:
                del self.boosts[i]
                self.score += 100
                self.cntr += 1

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
                        self.cntr = 0
            self.screen.fill((0, 0, 0))
            self.get_score()
            self.screen.blit(self.game_over_bg, (0, 0))
            f2 = pygame.font.SysFont('serif', 30)
            text2 = f2.render(str(self.score), False,
                              (255, 0, 0))
            self.screen.blit(text2, (350, 400))
            pygame.display.flip()
    def get_score(self):
        if self.cntr < 6:
            # в начале создается удаляется несколько платформ(чтобы их не считать создан cntr)
            if self.score < 0:
                self.score = 0
            elif self.score == 0:
                self.score = 0
            elif self.score > 0:
                self.score = 100


    def set_score(self):
        self.get_score()
        f2 = pygame.font.SysFont('serif', 20)
        text2 = f2.render(f'Счет: {str(self.score)}', False,
                        (255, 0, 0))
        self.screen.blit(text2, (500, 10))

    def play_again(self):
        app = App()
        app.start()
        pygame.display.flip()
        self.cntr = 0

    def start_scrn(self):
        while True:
            self.cc = 1
            self.screen.blit(self.start_screen, (0, 0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.start()

    def functions(self):
        self.clock.tick(60)
        self.check_play()
        self.screen.blit(self.bg, (0, 0))
        self.draw(self.boosts)
        self.pl.down(self.boosts)
        self.get_fps()
        self.set_score()

    def start(self):
        if self.cc != 1:
            self.start_scrn()
        self.cc = 1
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.play_again()
                break
            # пауза
            if keys[pygame.K_1]:
                self.pause_flag = True
                while self.pause_flag:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            exit()
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_2]:
                        self.pause_flag = False
                    font = pygame.font.SysFont("serif", 72)
                    text_paused = font.render("PAUSED", True, (255, 0, 0))
                    self.screen.blit(text_paused, (150, 250))
                    pygame.display.flip()
            # конец цикла с паузой
            if keys[pygame.K_LEFT]:
                self.pl.image = self.pl.pl_left
                self.pl.x -= 5
            if keys[pygame.K_RIGHT]:
                self.pl.image = self.pl.pl_right
                self.pl.x += 5
            self.functions()
            if self.pl.y > 800:
                self.lose_sound.play()
            if self.pl.y > 1000:
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

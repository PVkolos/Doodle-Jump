import pygame
import random
from boost import StaticBoost, RedBoost, MovementBoost
from player import *



class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load("images/doodlejump.PNG"))
        self.screen = pygame.display.set_mode((600, 800))
        self.bg = pygame.image.load("images/bg.jpg")
        self.game_over_bg = pygame.image.load('images/game_over_bg.jpg')
        self.start_screen = pygame.image.load("images/start_screen_bg.jpg")
        self.lose_sound = pygame.mixer.Sound('sfx/pada.mp3')
        self.start_sound = pygame.mixer.Sound('sfx/start.wav')
        self.boosts = [StaticBoost(100, 750), StaticBoost(300, 750), StaticBoost(500, 750)]
        self.pl = Player(self.screen)
        self.clock = pygame.time.Clock()
        self.flag = True
        self.pause_flag = False
        self.score = 0
        self.cntr = 0
        self.cc = 0
        self.running = True
        self.n_boosts = 20
        pygame.display.set_caption('DoodleJumpDemo')

    def draw(self, boosts):
        for boost in boosts:
            if type(boost) == MovementBoost:
                boost.update()
            self.screen.blit(boost.image, (boost.x - 60 / 2, boost.y))

    def check_play(self):
        if len(self.boosts) < self.n_boosts:
            while self.n_boosts - len(self.boosts) != 0:
                y = self.boosts[-1].y
                if not type(self.boosts[-1]) == StaticBoost:
                    for i in range(2, 15):
                        if type(self.boosts[-i]) == StaticBoost:
                            y = self.boosts[-i].y
                            break
                coord = (random.randint(80, 600 - 80),
                         random.randrange(round(y - 150), round(y), 5))
                a = 100
                while a != 0:
                    if self.check_collision(self.boosts, coord):
                        coord = (random.randint(80, 600 - 80),
                                 random.randrange(round(y - 150), round(y), 5))
                        a -= 1
                    else:
                        break
                if random.random() > 0.2:
                    bst = StaticBoost(coord[0], coord[1])
                elif random.random() > 0.1:
                    bst = RedBoost(coord[0], coord[1])
                else:
                    bst = MovementBoost(random.randint(100, 200), coord[1] + 5)
                self.boosts.append(bst)

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
        f2 = pygame.font.SysFont('al seana', 14)
        text2 = f2.render(f'FPS: {int(self.clock.get_fps() // 1)}', False,
                          (255, 0, 0))
        self.screen.blit(text2, (10, 10))

    @staticmethod
    def check_collision(items, item):
        for i in items:
            # if item.rect.colliderect(i.rect):
            #    return True
            if item[0] + 70 >= i.x and item[1] + 15 >= i.y:
                return True
        return False

    def game_over(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.restart()
            self.screen.fill((0, 0, 0))
            self.get_score()
            self.screen.blit(self.game_over_bg, (0, 0))
            f2 = pygame.font.SysFont('al seana', 30)
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
        f2 = pygame.font.SysFont('al seana', 30)
        text2 = f2.render(f'Score: {str(self.score)}', False,
                          (255, 0, 0))
        self.screen.blit(text2, (450, 10))

    def functions(self):
        self.clock.tick(60)
        self.check_play()
        self.screen.blit(self.bg, (0, 0))
        self.draw(self.boosts)
        self.pl.down(self.boosts)
        self.get_fps()
        self.set_score()

    def start(self):
        x = True
        if self.cc != 1:
            self.start_scrn()
        self.cc = 1
        self.running = True
        self.pl = Player(self.screen)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.restart()
            if keys[pygame.K_1] and not self.pause_flag:
                self.pause_flag = True
                self.pause()
            if keys[pygame.K_LEFT]:
                self.pl.image = self.pl.pl_left
                self.pl.x -= 5
            if keys[pygame.K_RIGHT]:
                self.pl.image = self.pl.pl_right
                self.pl.x += 5
            self.functions()
            if self.pl.y > 800:
                self.flag = False
                break
            pygame.display.flip()
        if self.pl.y > 800 and x:
            x = False
            self.lose_sound.play()
        if not self.flag:
            self.running = True
            self.game_over()
        else:
            pygame.quit()

    @staticmethod
    def restart():
        app = App()
        app.start()

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
                        self.start_sound.play()
                        self.start()

    def pause(self):
        while self.pause_flag and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_2]:
                    self.pause_flag = False
                self.screen.blit(self.bg, (0, 0))
                font = pygame.font.SysFont("al seana", 72)
                text_paused = font.render("PAUSED", True, (255, 0, 0))
                font = pygame.font.SysFont("al seana", 72)
                bestplayers = font.render("BEST PLAYERS", True, (255, 0, 0))
                self.screen.blit(text_paused, (210, 250))
                self.screen.blit(bestplayers, (130, 340))
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (150, 420, 300, 180))
                pygame.display.flip()


if __name__ == '__main__':
    app = App()
    app.start()

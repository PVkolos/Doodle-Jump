import random

import pygame

from player import *


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load("images/doodlejump.PNG"))
        pygame.display.set_caption('DoodleJumpDemo')
        self.screen = pygame.display.set_mode((600, 750))
        self.bg = pygame.image.load("images/bg.png")
        self.game_over_bg = pygame.image.load('images/game_over_bg.jpg')
        self.start_screen = pygame.image.load("images/start_screen_bg.png")
        self.pause_screen = pygame.image.load('images/pause.png')
        self.lose_sound = pygame.mixer.Sound('sfx/pada.mp3')
        self.start_sound = pygame.mixer.Sound('sfx/start.wav')
        self.boosts = [StaticBoost(100, 750), StaticBoost(300, 750), StaticBoost(500, 750)]
        self.bullets = []
        self.monsters = []
        self.pl = Player(self.screen)
        self.clock = pygame.time.Clock()
        self.score = 0
        self.cntr = 0
        self.cc = 0
        self.n_boosts = 20
        self.flag = True
        self.pause_flag = False
        self.running = True
        self.flag_monster = True

    def draw(self, boosts, bullets):
        for boost in boosts:
            if type(boost) == MovementBoost:
                boost.update()
            elif type(boost) == FederBoost:
                self.screen.blit(boost.get_image(), (boost.x - 60 / 2 + 30, boost.y - 35))
            self.screen.blit(boost.image, (boost.x - 60 / 2, boost.y))
        for bullet in bullets:
            self.screen.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
            bullet.update()

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
                bst = StaticBoost(coord[0], coord[1])
                if random.random() > 0.5:
                    if random.random() > 0.7:
                        bst = FederBoost(random.randint(100, 200), coord[1] + 5)
                    else:
                        bst = StaticBoost(coord[0], coord[1])
                elif random.random() > 0.7:
                    bst = RedBoost(coord[0], coord[1])
                elif random.random() > 0.9:
                    bst = MovementBoost(coord[0], coord[1])
                self.boosts.append(bst)

        if self.pl.rect.x < -80:
            self.pl.rect.x = 580
        elif self.pl.rect.x > 680:
            self.pl.rect.x = -40
        a = self.boosts.copy()
        for i in range(len(a)):
            if a[i].y > 800:
                del self.boosts[i]
                self.score += 100
                self.cntr += 1
        a = self.bullets.copy()
        for i in range(len(a)):
            if a[i].rect.y < -100:
                del self.bullets[i]

    def get_fps(self):
        f2 = pygame.font.SysFont('al seana', 14)
        text2 = f2.render(f'FPS: {int(self.clock.get_fps() // 1)}', False,
                          (255, 0, 0))
        self.screen.blit(text2, (10, 10))

    def get_results(self):
        pass

    @staticmethod
    def check_collision(items, item):
        for i in items:
            if item[0] + 70 >= i.x and item[1] + 15 >= i.y:
                return True
        return False

    def check_collision_monster_bullet(self):
        for monster in self.monsters:
            for bullet in self.bullets:
                if pygame.sprite.collide_mask(monster, bullet):
                    del self.monsters[0]
                    del self.bullets[self.bullets.index(bullet)]
                    self.flag_monster = True
                    break

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

    def draw_monster(self):
        for monster in self.monsters:
            monster.update()
            if pygame.sprite.collide_mask(monster, self.pl):
                self.game_over()
            self.screen.blit(monster.image, (monster.rect.x, monster.rect.y))
            if monster.rect.y > 800:
                del self.monsters[0]
                self.flag_monster = True

    def functions(self):
        self.clock.tick(60)
        self.check_play()
        self.screen.blit(self.bg, (0, 0))
        self.draw(self.boosts, self.bullets)
        self.pl.down(self.boosts, self.monsters)
        self.get_fps()
        self.set_score()
        self.check_collision_monster_bullet()
        self.draw_monster()

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.bullets.append(self.pl.shoot())
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.restart()
            if keys[pygame.K_1] and not self.pause_flag:
                self.pause_flag = True
                self.pause()
            if keys[pygame.K_LEFT]:
                self.pl.image = self.pl.pl_left
                self.pl.rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.pl.image = self.pl.pl_right
                self.pl.rect.x += 5
            self.functions()
            if self.pl.rect.y > 800:
                self.flag = False
                break
            pygame.display.flip()
            if self.score > 3000 and self.flag_monster:
                rnd = random.random()
                if rnd < 0.005:
                    self.monster()
        if self.pl.rect.y > 800 and x:
            self.lose_sound.play()
        if not self.flag:
            self.running = True
            self.game_over()
        else:
            pygame.quit()

    def monster(self):
        monster_ = Monster(250, -400)
        self.monsters.append(monster_)
        self.flag_monster = False

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
                self.screen.blit(self.pause_screen, (0, 0))
                # font = pygame.font.SysFont("al seana", 72)
                # text_paused = font.render("PAUSED", True, (255, 0, 0))
                # font = pygame.font.SysFont("al seana", 72)
                # best_players = font.render("BEST PLAYERS", True, (255, 0, 0))
                # self.screen.blit(text_paused, (210, 250))
                # self.screen.blit(best_players, (130, 340))
                # pygame.draw.rect(self.screen, (255, 255, 255), (150, 420, 300, 180))
                pygame.display.flip()


if __name__ == '__main__':
    app = App()
    app.start()
 

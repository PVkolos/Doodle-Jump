import random

from csv import writer

import csv
import pygame.display
from static import *
from player import *


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load("images/doodlejump.PNG"))
        pygame.display.set_caption('DoodleJumpDemo')
        self.screen = pygame.display.set_mode((600, 750))
        self.bg = pygame.image.load("images/bg.jpg")
        self.game_over_bg = pygame.image.load('images/game_over_bg.jpg')
        self.start_screen = pygame.image.load("images/start_screen_bg.jpg")
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
        self.player_name = ''
        self.pause_flag = False
        self.running = True
        self.flag_monster = True

    def draw(self, boosts: list, bullets: list):
        for boost in boosts:
            boost.update()
            boost.draw(self.screen)
        for bullet in bullets:
            bullet.update()
            bullet.draw(self.screen)
        for monster in self.monsters:
            monster.update()
            monster.draw(self.screen)

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
                if not self.flag_monster and pygame.sprite.collide_mask(self.monsters[0], self.pl):
                    self.game_over()
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
        if not self.flag_monster and self.monsters[0].rect.y > 800:
            del self.monsters[0]
            self.flag_monster = True

    def get_fps(self):
        f2 = pygame.font.SysFont('al seana', 14)
        text2 = f2.render(f'FPS: {int(self.clock.get_fps() // 1)}', False,
                          (100, 100, 100))
        self.screen.blit(text2, (10, 10))

    def get_results(self):
        flag = True
        r = csv.reader(open('results.csv'))
        lines = list(r)
        for i in lines:
            print(i)
            try:
                if i[0] == self.player_name:
                    flag = False
                    if int(i[1]) < self.score:
                        i[1] = self.score
                        writerr = csv.writer(open('results.csv', 'w'))
                        writerr.writerows(lines)
            except:
                pass

        if flag:
            if self.player_name != '':
                with open('results.csv', 'a', newline='') as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow([self.player_name, self.score])
                    f_object.close()

    def best_players_sort(self):
        all = []
        k = 0
        scr = []
        r = csv.reader(open('results.csv'))
        for i in list(r):
            try:
                all.append(i[0])
                all.append(int(i[1]))
            except:
                pass
        for j in all:
            try:
                if k % 2 == 1:
                    scr.append(int(j))
                k += 1
            except:
                pass
        scr = sorted(scr)
        try:
            self.best1 = (scr[-1], all[all.index(scr[-1]) - 1])
        except:
            pass
        try:
            self.best2 = (scr[-2], all[all.index(scr[-2]) - 1])
        except:
            pass
        try:
            self.best3 = (scr[-3], all[all.index(scr[-3]) - 1])
        except:
            pass

    def best_players_draw(self):
        font = pygame.font.SysFont("al seana", 32)
        self.best_players_sort()
        try:
            best_player1 = font.render("1: " + str(self.best1), True, (0, 0, 0))
            self.screen.blit(best_player1, (130, 250))
        except:
            pass
        try:
            best_player2 = font.render("2: " + str(self.best2), True, (0, 0, 0))
            self.screen.blit(best_player2, (130, 280))
        except:
            pass
        try:
            best_player3 = font.render("3: " + str(self.best3), True, (0, 0, 0))
            self.screen.blit(best_player3, (130, 310))
        except:
            pass

    def new_get_results(self):
        results = results_loader()
        if self.player_name:
            if self.player_name in results:
                if results[self.player_name] < self.score:
                    results[self.player_name] = self.score
            else:
                results[self.player_name] = self.score
            sorted_dict = {}
            sorted_keys = sorted(results, key=results.get)
            for w in sorted_keys:
                sorted_dict[w] = results[w]
            results_saver(sorted_dict)

    def set_results(self):
        font = pygame.font.SysFont("al seana", 32)
        results = results_loader()
        for i in range(1, len(results) + 1):
            self.screen.blit(font.render(f"{i}: " + list(results.keys())[-i], True, (0, 0, 0)), (130, 210 + 30 * i))

    @staticmethod
    def check_collision(items, item) -> bool:
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
        y = self.screen.get_size()[1]
        f2 = pygame.font.SysFont('al seana', 30)
        text2 = f2.render(str(self.score), False,
                          (255, 0, 0))
        # self.get_results()
        self.new_get_results()
        # self.best_players_sort()

        def check(boost):
            if boost.y < 0:
                del self.boosts[self.boosts.index(boost)]
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.restart()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.bg, (0, 0))
            self.pl.draw(self.screen)
            if self.boosts:
                for i in self.boosts:
                    i.y -= 20
                    i.draw(self.screen)
                    check(i)
                pygame.display.flip()
                continue
            if y > -10:
                self.screen.blit(self.game_over_bg, (0, y))
                self.screen.blit(text2, (350, y + 407))
                y -= 20
                self.pl.draw(self.screen)
                pygame.display.flip()
            else:
                self.screen.blit(self.game_over_bg, (0, 0))
                self.screen.blit(text2, (350, y + 415))
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
                          (100, 100, 100))
        self.screen.blit(text2, (450, 10))

    def functions(self):
        self.clock.tick(60)
        self.check_play()
        self.screen.blit(self.bg, (0, 0))
        self.draw(self.boosts, self.bullets)
        self.pl.down(self.boosts, self.monsters)
        self.get_fps()
        self.set_score()
        self.check_collision_monster_bullet()

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
            if self.score > 9000 and self.flag_monster:
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
        monster = Monster(250, -400)
        self.monsters.append(monster)
        self.flag_monster = False

    @staticmethod
    def restart():
        app = App()
        app.start()

    def start_scrn_draw(self):
        self.screen.blit(self.start_screen, (0, 0))
        font = pygame.font.SysFont("al seana", 62)
        name_text = font.render('name: ', True, (0, 0, 0))
        if self.player_name == '':
            enter_name = font.render('enter name', True, (128, 128, 128))
            self.screen.blit(enter_name, (260, 440))
        player_name_text = font.render(self.player_name, True, (0, 0, 0))
        self.screen.blit(player_name_text, (260, 440))
        self.screen.blit(name_text, (140, 440))

    def start_scrn(self):
        while True:
            self.cc = 1
            self.start_scrn_draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.start_sound.play()
                        self.start()
                    if event.key == pygame.K_RETURN:
                        self.start_sound.play()
                        self.start()
                        print(self.player_name)
                    if event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        if len(self.player_name) < 12:
                            self.player_name += event.unicode

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
                #self.best_players_draw()
                self.set_results()
                pygame.display.flip()


if __name__ == '__main__':
    app = App()
    app.start()

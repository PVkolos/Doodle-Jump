import random
import pygame.display
import image_manager
from static import *
from player import *
from boost import *
from image_manager import *


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(pygame.image.load("images/doodle-jump.png"))
        pygame.display.set_caption('DoodleJumpDemo')
        self.screen = pygame.display.set_mode((600, 750))
        self.bg = pygame.image.load(get_image('bg.png'))
        self.game_over_bg = pygame.image.load('game_over_bg.jpg')
        self.start_screen_bg = pygame.image.load("images/start_screen_bg.png")
        self.pause_screen_bg = pygame.image.load('images/pause.png')
        self.lose_sound = pygame.mixer.Sound('sfx/fall.mp3')
        self.start_sound = pygame.mixer.Sound('sfx/start.wav')
        self.boosts = pygame.sprite.Group()
        self.boosts.add(StaticBoost(100, 750))
        self.boosts.add(StaticBoost(300, 750))
        self.boosts.add(StaticBoost(500, 750))
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.pl = Player()
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

    def draw(self):
        self.boosts.update(self.screen)
        self.monsters.update()
        self.monsters.draw(self.screen)
        self.bullets.update()
        self.bullets.draw(self.screen)
        self.pl.draw(self.screen)

    def check_play(self):
        if len(self.boosts) < self.n_boosts:
            while self.n_boosts - len(self.boosts) != 0:
                a = self.boosts.sprites()
                y = a[-1].rect.y
                if not type(a[-1]) == StaticBoost:
                    for i in range(2, 15):
                        if type(self.boosts.sprites()[-i]) == StaticBoost:
                            y = self.boosts.sprites()[-i].rect.y
                            break
                coord = (random.randint(80, 600 - 80),
                         random.randrange(round(y - 150), round(y), 5))
                a = 100
                while a != 0:
                    if check_collision(self.boosts.sprites(), coord):
                        coord = (random.randint(80, 600 - 80),
                                 random.randrange(round(y - 150), round(y), 5))
                        a -= 1
                    else:
                        break
                monsters = self.monsters.sprites()
                # if not self.flag_monster and pygame.sprite.collide_mask(monsters[0], self.pl):
                #   self.game_over()
                if not self.flag_monster and pygame.sprite.collide_rect(monsters[0], self.pl):
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
                self.boosts.add(bst)
        if self.pl.rect.x < -80:
            self.pl.rect.x = 580
        elif self.pl.rect.x > 680:
            self.pl.rect.x = -40
        a = self.boosts.copy()
        for i in a:
            if i.rect.y > 800:
                self.boosts.remove(i)
                self.score += 100
                self.cntr += 1
        a = self.bullets.copy()
        for i in a:
            if i.rect.y < -100:
                self.bullets.remove(i)
        a = self.monsters.copy()
        for i in a:
            if not self.flag_monster and i.rect.y > 800:
                self.monsters.remove(i)
                self.flag_monster = True

    def get_fps(self):
        """
        Метод отрисовки фпс
        """
        f2 = pygame.font.Font('al-seana.ttf', 14)
        text2 = f2.render(f'FPS: {int(self.clock.get_fps() // 1)}', True,
                          (100, 100, 100))
        self.screen.blit(text2, (10, 10))

    def get_results(self):
        results = results_loader()
        if self.player_name:
            if self.player_name in results:
                if results[self.player_name] < self.score:
                    results[self.player_name] = self.score
            else:
                results[self.player_name] = self.score
            sorted_dict = {}
            sorted_keys = sorted(results, key=results.get)
            for i in sorted_keys:
                sorted_dict[i] = results[i]
            results_saver(sorted_dict)

    def set_results(self):
        font = pygame.font.Font("al-seana.ttf", 32)
        results = results_loader()
        if len(results) > 3:
            a = 3
        else:
            a = len(results)
        for i in range(1, a + 1):
            res = list(results.keys())[-i]
            self.screen.blit(font.render(f'{i}.{res}: {results.get(res)}', True, (0, 0, 0)), (130, 210 + 30 * i))

    def check_collision_monster_bullet(self):
        for monster in self.monsters:
            for bullet in self.bullets:
                if pygame.sprite.collide_mask(monster, bullet):
                    self.monsters = pygame.sprite.Group()
                    self.bullets.remove(bullet)
                    self.flag_monster = True
                    break

    def game_over(self):
        """
        Метод экрана проигрыша
        """
        self.lose_sound.play()
        y = self.screen.get_size()[1]
        f2 = pygame.font.Font('al-seana.ttf', 30)
        text2 = f2.render(str(self.score), True,
                          (255, 0, 0))
        self.get_results()
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
                self.boosts.update(self.screen)
                for i in self.boosts:
                    i.rect.y -= 20
                    if i.rect.y < 0:
                        self.boosts.remove(i)
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
                self.pl.rect.y += 20
                self.pl.draw(self.screen)
                pygame.display.flip()

    def get_score(self):
        """
        Метод для получения результата в начале
        """
        if self.cntr < 6:
            # в начале создается / удаляется несколько платформ(чтобы их не считать создан cntr)
            if self.score < 0:
                self.score = 0
            elif self.score == 0:
                self.score = 0
            elif self.score > 0:
                self.score = 100

    def set_score(self):
        """
        Метод отрисовки счета
        """
        self.get_score()
        f2 = pygame.font.Font('al-seana.ttf', 30)
        text2 = f2.render(f'Score: {str(self.score)}', True,
                          (100, 100, 100))
        self.screen.blit(text2, (450, 10))

    def functions(self):
        self.clock.tick(60)
        self.check_play()
        self.screen.blit(self.bg, (0, 0))
        self.draw()
        self.pl.down(self.boosts, self.monsters)
        self.screen.blit(pygame.image.load('images/classic/paused.png'), (20, 20))
        self.get_fps()
        self.set_score()
        self.check_collision_monster_bullet()

    def start(self):
        if self.cc != 1:
            self.start_screen()
        self.cc = 1
        self.running = True
        self.pl = Player()
        while self.running:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (20 < mouse[0] < 20 + 100) and (20 < mouse[1] < 20 + 36):
                        self.button_paused()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.bullets.add(self.pl.shoot())
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.restart()
            if keys[pygame.K_1] and not self.pause_flag:
                self.pause_flag = True
                self.pause()
            if keys[pygame.K_3]:
                image_manager.is_snow = True
                self.pl.update_images()
                self.bg = pygame.image.load(get_image('bg.png'))
            if keys[pygame.K_4]:
                image_manager.is_snow = False
                self.pl.update_images()
                self.bg = pygame.image.load(get_image('bg.png'))
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
        if not self.flag:
            self.running = True
            self.game_over()
        else:
            pygame.quit()

    def monster(self):
        monster = Monster(250, -400)
        self.monsters.add(monster)
        self.flag_monster = False

    def restart(self):
        """
        Метод для перезапуска
        """
        self.boosts = pygame.sprite.Group()
        self.boosts.add(StaticBoost(100, 750))
        self.boosts.add(StaticBoost(300, 750))
        self.boosts.add(StaticBoost(500, 750))
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.pl = Player()
        self.score = 0
        self.cntr = 0
        self.cc = 0
        self.n_boosts = 20
        self.flag = True
        self.player_name = ''
        self.pause_flag = False
        self.running = True
        self.flag_monster = True
        self.start()

    def button_theme(self):
        mouse = pygame.mouse.get_pos()
        width = 100
        height = 36
        x = 20
        y = 200
        image = pygame.image.load('images/classic/theme.png')
        image2 = pygame.image.load('images/classic/theme2.png')
        pygame.draw.rect(self.screen, (247, 243, 231), (x, y, width, height))
        if image_manager.is_snow:
            self.screen.blit(image2, (20, 200))
        else:
            self.screen.blit(image, (20, 200))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and (x < mouse[0] < x + width) and (y < mouse[1] < y + height):
                if not image_manager.is_snow:
                    image_manager.is_snow = True
                elif image_manager.is_snow:
                    image_manager.is_snow = False
                self.bg = pygame.image.load(get_image('bg.png'))
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

    def button_paused(self):
        self.pause_flag = True
        self.pause()

    def start_screen_draw(self):
        """
        Метод для функций на главном экране
        """
        self.screen.blit(self.start_screen_bg, (0, 0))
        self.button_theme()
        font = pygame.font.Font("al-seana.ttf", 62)
        name_text = font.render('name: ', True, (0, 0, 0))
        if self.player_name == '':
            enter_name = font.render('enter name', True, (128, 128, 128))
            self.screen.blit(enter_name, (260, 360))
        player_name_text = font.render(self.player_name, True, (0, 0, 0))
        self.screen.blit(player_name_text, (260, 360))
        self.screen.blit(name_text, (140, 360))

    def start_screen(self):
        """
        метод для экрана старта
        """
        while True:
            self.cc = 1
            self.start_screen_draw()
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
        """
        метод для экрана паузы
        """
        while self.pause_flag and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_2]:
                    self.pause_flag = False
                self.screen.blit(self.bg, (0, 0))
                self.screen.blit(self.pause_screen_bg, (0, 0))
                image = pygame.image.load('images/classic/paused.png')
                self.screen.blit(image, (20, 20))
                self.set_results()
                mouse = pygame.mouse.get_pos()
                if (20 < mouse[0] < 20 + 100) and (20 < mouse[1] < 20 + 36):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.pause_flag = False
                pygame.display.flip()


if __name__ == '__main__':
    App().start()

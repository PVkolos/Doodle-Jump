import random
import pygame.display
from static import *
from player import *
from boost import *
from file_manager import *
from screen import Start, Pause


class App:
    def __init__(self):
        pygame.display.set_icon(pygame.image.load(get_image('doodle-jump.png')))
        pygame.display.set_caption('DoodleJumpDemo')
        self.screen = pygame.display.set_mode((600, 800))
        self.bg = pygame.image.load(get_image('bg.png'))
        self.game_over_bg = pygame.image.load(get_image('game_over_bg.jpg'))
        self.start_screen_bg = pygame.image.load(get_image('start_screen_bg.png'))
        self.pause_screen_bg = pygame.image.load(get_image('pause.png'))
        self.lose_sound = pygame.mixer.Sound('sfx/fall.mp3')
        self.start_sound = pygame.mixer.Sound('sfx/start.wav')
        self.boosts = pygame.sprite.Group()
        self.boosts.add(StaticBoost(500, 750))
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.pl = Player()
        self.clock = pygame.time.Clock()
        self.score = 0
        self.cntr = 0
        self.n_boosts = 20
        self.player_name = ''
        self.flag_monster = True
        self.fps = 60

    def draw(self):
        self.boosts.update(self.screen)
        self.monsters.update()
        self.monsters.draw(self.screen)
        self.bullets.update()
        self.bullets.draw(self.screen)
        self.pl.draw(self.screen)

    def check_play(self):
        if self.pl.rect.x < -80:
            self.pl.rect.x = 580
        elif self.pl.rect.x > 680:
            self.pl.rect.x = -40
        for i in self.boosts.copy():
            if i.rect.y > 800:
                self.boosts.remove(i)
                self.score += 100
        for i in self.bullets.copy():
            if i.rect.y < -100:
                self.bullets.remove(i)
        for i in self.monsters.copy():
            if not self.flag_monster and i.rect.y > 800:
                self.monsters.remove(i)
                self.flag_monster = True

    def generate_level(self):
        if self.score > 9000 and self.flag_monster:
            rnd = random.random()
            if rnd < 0.005:
                self.monster()
        while len(self.boosts) < self.n_boosts:
            coord = [random.randint(80, 520), self.boosts.sprites()[-1].rect.y - random.randint(50, 80)]
            if self.cntr:
                if self.boosts.sprites()[-1].rect.x not in range(80, 194):
                    coord = [random.randint(80, 194), self.boosts.sprites()[-1].rect.y - random.randint(25, 50)]
                elif self.boosts.sprites()[-1].rect.x not in range(406, 520):
                    coord = [random.randint(406, 520), self.boosts.sprites()[-1].rect.y - random.randint(25, 50)]
                i = self.get_random_boost()
                bst = i(coord[0], coord[1])
                self.cntr = 0
            else:
                self.cntr = 1
                bst = self.get_random_boost()(coord[0], coord[1])
            self.boosts.add(bst)

    @staticmethod
    def get_random_boost():
        boosts = [StaticBoost, StaticBoost, StaticBoost, StaticBoost, StaticBoost,
                  RedBoost, RedBoost, MovementBoost, FederBoost, FederBoost]
        return random.choice(boosts)

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
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    return
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

    def set_score(self):
        """
        Метод отрисовки счета
        """
        f2 = pygame.font.Font('al-seana.ttf', 30)
        text2 = f2.render(f'Score: {str(self.score)}', True,
                          (100, 100, 100))
        self.screen.blit(text2, (450, 10))

    def functions(self):
        self.check_play()
        self.generate_level()
        self.screen.blit(self.bg, (0, 0))
        self.draw()
        self.pl.down(self.boosts, self.monsters)
        self.screen.blit(pygame.image.load(get_image('paused.png')), (20, 20))
        self.get_fps()
        self.set_score()
        self.check_collision_monster_bullet()

    def start(self):
        self.restart()
        self.start_sound.play()
        self.pl = Player()
        while True:
            self.clock.tick(self.fps)
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
                return
            if keys[pygame.K_1]:
                self.pause()
            if keys[pygame.K_3]:
                change_theme()
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
                return self.game_over()
            if not self.flag_monster and pygame.sprite.collide_rect(self.monsters.sprites()[0], self.pl):
                return self.game_over()
            pygame.display.flip()

    def monster(self):
        monster = Monster(250, -400)
        self.monsters.add(monster)
        self.flag_monster = False

    def restart(self):
        """
        Метод для перезапуска
        """
        self.boosts.empty()
        self.boosts.add(StaticBoost(500, 750))
        self.bullets.empty()
        self.monsters.empty()
        self.pl = Player()
        self.score = 0
        self.cntr = 0
        self.n_boosts = 20
        self.flag_monster = True

    def button_paused(self):
        self.pause()

    def start_scene(self):
        """
        метод для экрана старта
        """
        start = Start(self.screen)
        while True:
            self.clock.tick(self.fps)
            for event in start.get_event():
                if event == 'start':
                    self.player_name = start.name
                    self.bg = pygame.image.load(get_image('bg.png'))
                    self.start()
            start.draw()

    def pause(self):
        """
        метод для экрана паузы
        """
        pause = Pause(self.screen)
        pause.draw()
        while True:
            self.clock.tick(self.fps)
            for event in pause.get_event():
                if event == 'start':
                    return


if __name__ == '__main__':
    pygame.init()
    App().start_scene()

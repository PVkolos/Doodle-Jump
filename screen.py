import pygame
from widgets import CheckButton, PushButton
from static import results_loader
from file_manager import get_image, change_theme, get_snow, get_path
import sys


class Screen:
    def __init__(self, screen):
        self.objects = []
        self.screen = screen
        self.bg = None
        self.font = pygame.font.Font(get_path('al-seana.ttf'), 62)


class Pause(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.bg = pygame.image.load(get_image('pause.png'))
        self.init_objects()
        self.font = pygame.font.Font(get_path('al-seana.ttf'), 32)

    def init_objects(self):
        x = PushButton(100, 36, 20, 20)
        x.def_image = pygame.image.load(get_image('paused.png'))
        self.objects.append(x)

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.update()
                return ['start']
        return []

    def update(self):
        for i in self.objects:
            i.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        results = results_loader()
        if len(results) > 3:
            a = 3
        else:
            a = len(results)
        for i in range(1, a + 1):
            res = list(results.keys())[-i]
            self.screen.blit(self.font.render(f'{i}.{res}: {results.get(res)}', True, (0, 0, 0)), (130, 210 + 30 * i))
        pygame.display.flip()


class Start(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.bg = pygame.image.load(get_image('start_screen_bg.png'))
        self.name = ''
        self.init_objects()

    def init_objects(self):
        x = CheckButton(100, 36, 20, 200)
        x.def_image = pygame.image.load(get_image('theme.png'))
        x.check_image = pygame.image.load(get_image('theme2.png'))
        x.connect(change_theme)
        x.set_checked(get_snow())
        x.update()
        self.objects.append(x)

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.objects:
                    i.click_check()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return ['start']
                if event.key == pygame.K_RETURN:
                    return ['start']
                if event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                else:
                    if len(self.name) < 12:
                        self.name += event.unicode
        return []

    def update(self):
        for i in self.objects:
            i.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        name_text = self.font.render('name: ', True, (0, 0, 0))
        enter_name = self.font.render('enter name', True, (128, 128, 128))
        if self.name == '':
            self.screen.blit(enter_name, (260, 360))
        player_name_text = self.font.render(self.name, True, (0, 0, 0))
        self.screen.blit(player_name_text, (260, 360))
        self.screen.blit(name_text, (140, 360))
        for i in self.objects:
            i.draw(self.screen)
        pygame.display.flip()

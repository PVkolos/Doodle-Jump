import image_manager
import pygame
from widgets import CheckButton


class Screen:
    def __init__(self, screen):
        self.objects = []
        self.screen = screen
        self.bg = None
        self.font = pygame.font.Font("al-seana.ttf", 62)


class Pause(Screen):
    def __init__(self, screen):
        super().__init__(screen)


class GameOver(Screen):
    def __init__(self, screen):
        super().__init__(screen)


class Start(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.bg = pygame.image.load("images/start_screen_bg.png")
        self.name = ''
        self.init_objects()

    def init_objects(self):
        x = CheckButton(100, 36, 20, 200)
        x.def_image = pygame.image.load('images/classic/theme.png')
        x.check_image = pygame.image.load('images/classic/theme2.png')
        self.objects.append(x)

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.update()
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
            for event in i.get_event():
                if event == 'clicked':
                    image_manager.change_theme()

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
            i.update()
            i.draw(self.screen)
        pygame.display.flip()

import pygame
import sys
import requests
import io

W_HEIGHT, W_WIDTH = 600, 799


def get_picture(pos, delta, mode=0):
    requ = 'http://static-maps.yandex.ru/1.x/?ll=%f,%f&spn=%f,%f&l=%s' %\
           (pos[0], pos[1], delta[0], delta[1], ['map', 'sat', 'hybrid'][mode])
    answ = requests.get(requ)
    if answ:
        return pygame.image.load(io.BytesIO(answ.content))
    else:
        print('lol! Something goes wrong.')
        sys.exit(1)


class Inputer:
    def __init__(self, game, pos, height_width, background_color=(70, 70, 220),
                 text_color=(255, 255, 254), title='Input here'):
        self.game = game
        self.text = ''
        self.pos = tuple(pos)
        self.hw = tuple(height_width)
        self.bg_color = background_color
        self.tx_color = text_color
        self.text_surf = None
        self.text_surf_update()
        self.title = game.font.render(title, False, text_color)

        self.game.objects.append(self)
        self.enter = False

        self.d = 0
        self.d1 = 20

    def update(self):
        for i in self.game.eventolist:
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if 0 <= self.game.mouse_pos[0] - self.pos[0] <= self.hw[1]:
                        if 0 <= self.game.mouse_pos[1] - self.pos[1] <= self.hw[0]:
                            self.enter = True
                            continue
                self.enter = False
            if i.type == pygame.KEYDOWN:
                if i.unicode in 'qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM,.':
                    self.text = self.text + i.unicode
                    self.text_surf_update()
                elif i.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.text_surf_update()
        if self.enter:
            self.d += 1 if self.d < self.d1 else - self.d1

    def text_surf_update(self):
        self.text_surf = self.game.font.render(self.text, 1, self.tx_color)

    def draw(self):
        pygame.draw.rect(self.game.img, (254, 254, 254), (*self.pos, *self.hw[::-1]), 2)
        pygame.draw.rect(self.game.img, self.bg_color if not self.enter else
                                        tuple(map(lambda a: a + 20, self.bg_color)),
                         (self.pos[0] + 3, self.pos[1] + 3, self.hw[1] - 6, self.hw[0] - 6))
        self.title.blit(self.game.img, (self.pos[0], self.pos[1] - 20))
        if self.enter and 0 < self.d < 10:
            ll = self.text_surf.get_width() + 2
            pygame.draw.line(self.game.img,
                             self.tx_color, (self.pos[0] + ll, self.pos[1] + 2),
                             (self.pos[0] + ll, self.pos[1] + self.hw[0] - 2), 2)
        self.game.img.blit(self.text_surf, self.pos)


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 20)
        self.canvas = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
        self.timer = pygame.time.Clock()

        self.running = True
        self.img = pygame.Surface((W_WIDTH, W_HEIGHT))

        self.mouse_pos = (0, 0)

        self.objects = []
        self.eventolist = []

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.eventolist = pygame.event.get()
        for i in self.eventolist:
            if i.type == pygame.QUIT:
                self.running = False
        for i in self.objects:
            i.update()
        self.draw()
        pygame.display.flip()

    def draw(self):
        self.img.fill((20, 20, 200))
        pygame.draw.rect(self.img, (254, 254, 254), (20, 20, 400, 320), 2)
        for i in self.objects:
            i.draw()

        self.canvas.blit(self.img, (0, 0))

    def main_(self):
        while self.running:
            self.update()
            self.timer.tick(50)


if __name__ == '__main__':
    game = Game()
    Inputer(game, (450, 20), (20, 299))
    game.main_()

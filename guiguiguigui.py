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


class Scroller:
    def __init__(self, game, pos, height_width, background_color=(70, 70, 220),
                 valve_getter=lambda: 1, valve_diap=(0, 1)):
        self.game = game
        self.pos = tuple(pos)
        self.hw = tuple(height_width)
        self.bg_color = background_color

        self.game.objects.append(self)
        self.enter = False

        self.valve_getter = valve_getter
        self.valve_diap = valve_diap

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.game.img, (254, 254, 254), (*self.pos, *self.hw[::-1]), 2)
        pygame.draw.rect(self.game.img, self.bg_color,
                         (self.pos[0] + 3, self.pos[1] + 3, self.hw[1] - 6, self.hw[0] - 6))
        valve = self.valve_getter()
        valve = max(min(self.valve_diap[1], valve), self.valve_diap[0]) / (-self.valve_diap[0] + self.valve_diap[1])
        pygame.draw.circle(self.game.img, (220, 220, 220), (self.pos[0] + self.hw[0] // 2 +
                                                            int(valve * (self.hw[1] - self.hw[0])),
                                                            self.pos[1] + self.hw[0] // 2), self.hw[0] // 2 - 3)


class Button:
    def __init__(self, game, pos, height_width, background_color=(70, 70, 220),
                 text_color=(255, 255, 254), title='BUTTON, DO NOT PRESS', action=None):
        self.game = game
        self.pos = tuple(pos)
        self.hw = tuple(height_width)
        self.bg_color = background_color
        self.tx_color = text_color
        self.title = game.font.render(title, False, text_color)

        self.game.objects.append(self)
        self.enter = False

        self.action = action

    def update(self):
        for i in self.game.eventolist:
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1:
                    if 0 <= self.game.mouse_pos[0] - self.pos[0] <= self.hw[1]:
                        if 0 <= self.game.mouse_pos[1] - self.pos[1] <= self.hw[0]:
                            self.enter = True
                            if self.action is not None:
                                self.action()
                            return
        self.enter = False

    def draw(self):
        pygame.draw.rect(self.game.img, (254, 254, 254), (*self.pos, *self.hw[::-1]), 2)
        pygame.draw.rect(self.game.img, self.bg_color if not self.enter else
        tuple(map(lambda a: a + 20, self.bg_color)),
                         (self.pos[0] + 3, self.pos[1] + 3, self.hw[1] - 6, self.hw[0] - 6))
        hw, hh = self.title.get_width() // 2, self.title.get_height() // 2
        self.game.img.blit(self.title, (self.pos[0] + self.hw[1] // 2 - hw, self.pos[1] + self.hw[0] // 2 - hh))

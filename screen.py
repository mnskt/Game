from fighter import *
from enum import Enum
import pygame


pygame.init()
clock = pygame.time.Clock()
fps = 60

BOT_PANEL_HEIGHT = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400 + BOT_PANEL_HEIGHT

pygame.display.set_caption('Synergy')
FONT = pygame.font.SysFont(name='Times New Roman', size=26)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

SPEED = 6


class Setup:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bg_paths = [f'img/Background/parallax_forest/{name}.png' for name in range(1, 4)]
        self.bg_layers: list = []
        for idx, layer in enumerate(self.bg_paths):
            self.bg_layers.append(pygame.image.load(layer).convert_alpha())
            self.bg_layers[idx] = pygame.transform.scale(
                self.bg_layers[idx],
                (
                    self.bg_layers[idx].get_width() * 3,
                    self.bg_layers[idx].get_height() * 3
                )
            )
        self.bg_img_mid_offset = 0
        self.bg_img_back_offset = 0
        self.bg_img_front_offset = 0

        self.panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
        # Health bar
        self.bar_outline_img = pygame.image.load('img/UI/bar.png').convert_alpha()
        self.bar_outline_img = pygame.transform.scale(self.bar_outline_img,
                                                      (self.bar_outline_img.get_width() * 3,
                                                       self.bar_outline_img.get_height() * 3))
        self.bar_bg_img = pygame.image.load('img/UI/bar_background.png').convert_alpha()
        self.bar_bg_img = pygame.transform.scale(self.bar_bg_img,
                                                 (self.bar_bg_img.get_width() * 3, self.bar_bg_img.get_height() * 3))
        self.bar_fg_img = pygame.image.load('img/UI/health_bar.png').convert_alpha()


class Layers(Enum):
    FRONT = 0
    MIDDLE = 1
    BACK = 2


class Screen(Setup):
    def __init__(self):
        super().__init__()
        self.att_anim_counter = 0

    def draw_bg(self, x: int, y: int, offset_mid: int, offset_back: int, offset_front: int):
        for idx, layer in enumerate(self.bg_layers):
            if idx == Layers.FRONT.value:
                self.screen.blit(layer, (x + offset_back, y))
                self.screen.blit(layer, (x + offset_back + SCREEN_WIDTH, y))
                self.screen.blit(layer, (x + offset_back - SCREEN_WIDTH, y))
            if idx == Layers.MIDDLE.value:
                self.screen.blit(layer, (x + offset_mid, y))
                self.screen.blit(layer, (x + offset_mid + SCREEN_WIDTH, y))
                self.screen.blit(layer, (x + offset_mid - SCREEN_WIDTH, y))
            if idx == Layers.BACK.value:
                self.screen.blit(layer, (x + offset_front, y))
                self.screen.blit(layer, (x + offset_front + SCREEN_WIDTH, y))
                self.screen.blit(layer, (x + offset_front - SCREEN_WIDTH, y))

    def draw_text(self, text: str, font, text_color: tuple[int, int, int], x, y):
        img = font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def draw_panel(self, x, y):
        self.screen.blit(self.panel_img, (x, y))

    def draw_health_bar(self, x, y, fighter):
        self.draw_text(text=f'{fighter.name} HP: {int(fighter.hp)}',
                       font=FONT, text_color=RED, x=SCREEN_WIDTH / 6, y=SCREEN_HEIGHT - BOT_PANEL_HEIGHT + 50)
        # Show player stats
        self.screen.blit(self.bar_bg_img, (x, y))
        fighter = pygame.transform.scale(self.bar_fg_img,
                                         (((fighter.hp / fighter.max_hp) * 100) * 3, self.bar_fg_img.get_height() * 3))
        self.screen.blit(fighter, (x, y))
        self.screen.blit(self.bar_outline_img, (x - 27, y - 9))

    def handle_inputs(self, keys, knight, f_hit: bool, is_running: bool):
        if keys[pygame.K_ESCAPE]:
            is_running = False
        if keys[pygame.K_d]:
            knight.orientation = 'Right'
            self.bg_img_mid_offset -= 0.4 * SPEED
            self.bg_img_back_offset -= 0.2 * SPEED
            self.bg_img_front_offset -= 0.6 * SPEED
        elif keys[pygame.K_a]:
            knight.orientation = 'Left'
            self.bg_img_mid_offset += 0.4 * SPEED
            self.bg_img_back_offset += 0.2 * SPEED
            self.bg_img_front_offset += 0.6 * SPEED

        if keys[pygame.K_SPACE]:
            knight.action = 1
            knight.frame_index = 0
            f_hit = True
        if f_hit:
            self.att_anim_counter += 1
        return f_hit, is_running

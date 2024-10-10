from enum import Enum
from pathlib import WindowsPath
import pygame


FPS = 60

BOT_PANEL_HEIGHT = 150
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400 + BOT_PANEL_HEIGHT

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

SPEED = 6


class Setup:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Synergy')
        self.font = WindowsPath('fonts/font.ttf')
        self.font = pygame.font.Font(self.font, size=20)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.bg_img_path = WindowsPath('img/Background/parallax_forest')
        self.panel_img_path = WindowsPath(f'{self.bg_img_path.parent.parent}/Icons/panel.png')
        self.bar_outline_img_path = WindowsPath(f'{self.bg_img_path.parent.parent}/UI/bar.png')
        self.bar_bg_img_path = WindowsPath(f'{self.bar_outline_img_path.parent}/bar_background.png')
        self.bar_fg_img_path = WindowsPath(f'{self.bar_bg_img_path.parent}/health_bar.png')

        self.bg_paths = [f'{self.bg_img_path}/{name}.png' for name in range(1, 5)]
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
        self.bg_img_ground_offset = 0

        self.panel_img = pygame.image.load(self.panel_img_path).convert_alpha()
        # Health bar
        self.bar_outline_img = pygame.image.load(self.bar_outline_img_path).convert_alpha()
        self.bar_outline_img = pygame.transform.scale(self.bar_outline_img,
                                                      (self.bar_outline_img.get_width() * 3,
                                                       self.bar_outline_img.get_height() * 3))
        self.bar_bg_img = pygame.image.load(self.bar_bg_img_path).convert_alpha()
        self.bar_bg_img = pygame.transform.scale(self.bar_bg_img,
                                                 (self.bar_bg_img.get_width() * 3, self.bar_bg_img.get_height() * 3))
        self.bar_fg_img = pygame.image.load(self.bar_fg_img_path).convert_alpha()


class Layers(Enum):
    FRONT = 0
    MIDDLE = 1
    BACK = 2
    GROUND = 3


class Screen(Setup):
    def __init__(self):
        super().__init__()
        self.att_anim_counter = 0

    def _blit_bg(self, layer: pygame.Surface, x: int, y: int, offset: int):
        """
        Method draws passed background layer 3 times. One in the middle of the screen, and two more
        on either side off-screen.

        :param layer: Background layer.
        :param x: x coordinate of the bg layer.
        :param y: y coordinate of the bg layer.
        :param offset: offset at which the bg layer will be drawn.
        """
        self.screen.blit(layer, (x + offset, y))
        self.screen.blit(layer, (x + offset + SCREEN_WIDTH, y))
        self.screen.blit(layer, (x + offset - SCREEN_WIDTH, y))

    def draw_bg(self, x: int, y: int | float, offset_mid: int, offset_back: int, offset_front: int, offset_ground: int):
        """
        Method draws the background layers, one after the other.

        :param x: x coordinate of the bg layer.
        :param y: y coordinate of the bg layer.
        :param offset_mid: middle layer offset at which the bg layer will be drawn.
        :param offset_back: back layer offset at which the bg layer will be drawn.
        :param offset_front: front layer offset at which the bg layer will be drawn.
        """
        for idx, layer in enumerate(self.bg_layers):
            if idx == Layers.FRONT.value:
                self._blit_bg(layer=layer, x=x, y=y, offset=offset_back)
            if idx == Layers.MIDDLE.value:
                self._blit_bg(layer=layer, x=x, y=y, offset=offset_mid)
            if idx == Layers.BACK.value:
                self._blit_bg(layer=layer, x=x, y=y, offset=offset_front)
            if idx == Layers.GROUND.value:
                self._blit_bg(layer=layer, x=x, y=y+375, offset=offset_ground)

    def draw_text(self, text: str, font, text_color: tuple[int, int, int], x: int | float, y: int | float):
        """
        Method draw provided text at the specified location coordinates.

        :param text: Text to be drawn.
        :param font: Font which to use for the text.
        :param text_color: Color which to use for the text.
        :param x: x coordinate of the text.
        :param y: y coordinate of the text.
        """
        img = font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def draw_panel(self, x: int | float, y: int | float):
        """
        Method draws the bottom panel.

        :param x: x coordinate of the panel.
        :param y: y coordinate of the panel.
        """
        self.screen.blit(self.panel_img, (x, y))

    def draw_health_bar(self, x: int | float, y: int | float, fighter):
        """
        Method draws the health bar and contains logic to reduce the bar size based on the HP
        of the fighter.

        :param x: x coordinate of the panel.
        :param y: y coordinate of the panel.
        :param fighter: Fighter containing information for the health bar.
        """
        temp_fighter = fighter
        # Show player stats
        self.screen.blit(self.bar_bg_img, (x, y))
        fighter = pygame.transform.scale(self.bar_fg_img,
                                         (((fighter.hp / fighter.max_hp) * 100) * 3, self.bar_fg_img.get_height() * 3))
        self.screen.blit(fighter, (x, y))
        self.screen.blit(self.bar_outline_img, (x - 27, y - 9))
        self.draw_text(text=f'{int(temp_fighter.hp)}/{int(temp_fighter.max_hp)}',
                       font=self.font, text_color=WHITE,
                       x=SCREEN_WIDTH / 6 + 40, y=SCREEN_HEIGHT - BOT_PANEL_HEIGHT + 13)
        del temp_fighter

    def handle_inputs(self, keys, knight, f_hit: bool, is_running: bool):
        """
        Method handles all user keyboard inputs and contains logic for moving the fighter
        movement, game quitting etc.

        :param keys: Pressed keys.
        :param knight: Fighter whose moves are evaluated.
        :param f_hit: Check if "F" key was hit.
        :param is_running: Variable for determining main loop status.
        """

        if keys[pygame.K_ESCAPE]:
            is_running = False
        if keys[pygame.K_d] and not f_hit:
            knight.orientation = 'Right'
            knight.action = 1
            self.bg_img_mid_offset -= 0.4 * SPEED
            self.bg_img_back_offset -= 0.2 * SPEED
            self.bg_img_front_offset -= 0.6 * SPEED
            self.bg_img_ground_offset -= 0.8 * SPEED
            movement_key_hit = True
        elif keys[pygame.K_a] and not f_hit:
            knight.orientation = 'Left'
            knight.action = 1
            self.bg_img_mid_offset += 0.4 * SPEED
            self.bg_img_back_offset += 0.2 * SPEED
            self.bg_img_front_offset += 0.6 * SPEED
            self.bg_img_ground_offset += 0.8 * SPEED
            movement_key_hit = True
        else:
            movement_key_hit = False

        if keys[pygame.K_SPACE]:
            if self.att_anim_counter == 0:
                knight.action = 2
                knight.frame_index = 0
                f_hit = True
        if self.att_anim_counter >= 20:
            self.att_anim_counter = 0
            knight.action = 0
            knight.frame_index = 0
            f_hit = False
        if f_hit:
            self.att_anim_counter += 1

        if not movement_key_hit and not f_hit:
            knight.action = 0
            if knight.frame_index >= len(knight.animation_list[knight.action]):
                knight.frame_index = 0
        return f_hit, is_running

    def handle_parallax(self):
        """
        Method handles the parallax effect for the background.
        """
        if self.bg_img_front_offset <= -SCREEN_WIDTH:
            self.bg_img_front_offset = SCREEN_WIDTH
        elif self.bg_img_front_offset >= SCREEN_WIDTH:
            self.bg_img_front_offset = -SCREEN_WIDTH

        if self.bg_img_mid_offset <= -SCREEN_WIDTH:
            self.bg_img_mid_offset = 0
        elif self.bg_img_mid_offset >= SCREEN_WIDTH:
            self.bg_img_mid_offset = 0

        if self.bg_img_back_offset <= -SCREEN_WIDTH:
            self.bg_img_back_offset = 0
        elif self.bg_img_back_offset >= SCREEN_WIDTH:
            self.bg_img_back_offset = 0

        if self.bg_img_ground_offset <= -SCREEN_WIDTH:
            self.bg_img_ground_offset = SCREEN_WIDTH
        elif self.bg_img_ground_offset >= SCREEN_WIDTH:
            self.bg_img_ground_offset = -SCREEN_WIDTH

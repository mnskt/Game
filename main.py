from fighter import *
from screen import Screen


ENEMY_INIT_LOC = 750

f_hit = False

screen = Screen()
knight = Fighter(x=200, y=320, offset=0, name='Knight', max_hp=30)
# enemy_1 = Fighter(x=ENEMY_INIT_LOC, offset=0, y=330, name='Bandit', max_hp=15, strength=5, potions=1)
# enemy_2 = Fighter(x=int(ENEMY_INIT_LOC-enemy_1.image.get_width()/1.5),
#                   offset=0, y=330, name='Bandit', max_hp=15, strength=5, potions=1)
#
# enemy_list = [enemy_1, enemy_2]

is_running = True
i = 0
while is_running:
    screen.clock.tick(FPS)
    screen.screen.fill((0, 0, 0))
    screen.draw_bg(x=0, y=0, offset_mid=screen.bg_img_mid_offset,
                   offset_back=screen.bg_img_back_offset,
                   offset_front=screen.bg_img_front_offset)
    screen.handle_parallax()
    screen.draw_panel(x=0, y=SCREEN_HEIGHT - BOT_PANEL_HEIGHT)
    screen.draw_health_bar(x=BOT_PANEL_HEIGHT / 2 - 23, y=SCREEN_HEIGHT - BOT_PANEL_HEIGHT + 19, fighter=knight)

    # for idx, enemy in enumerate(enemy_list):
    #     enemy.draw_fighter()

    knight.update()
    knight.draw_fighter()

    # for enemy in enemy_list:
    #     enemy.update()
    #     enemy.draw_fighter()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
    keys = pygame.key.get_pressed()
    f_hit, is_running = screen.handle_inputs(keys=keys, knight=knight, f_hit=f_hit, is_running=is_running)

    pygame.display.update()
pygame.quit()

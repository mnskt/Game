from screen import *
from fighter_animation_parse_from_tile_set import ParseTileSet


class Fighter(Screen):

    animations = {
        'Idle': 7,
        'Run': 9,
        'Attack': 7,
    }
    cls_frame_list =[]
    cls_action = 0

    def __init__(self, x: float, y: int, offset: int, name: str, max_hp: int, img_folder_name: str, tile_set: bool):
        super().__init__()
        self.tile_set = tile_set
        self.animation_list = []
        if tile_set:
            parse = ParseTileSet(frame_height=80, img_folder_name=img_folder_name)
            self.animation_list = parse.create_frame_list()
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.frame_index = 0
        self.action = 0  # 0: Idle, 1: Run, 2: Attack
        self.update_time = pygame.time.get_ticks()
        self.x = x
        self.y = y
        self.offset = offset
        self.orientation = 'Right'
        if not tile_set:
            for animation, count in self.animations.items():
                temp_img_list = []
                for frame in range(count):
                    img = pygame.image.load(f'img/{self.name}/{animation}/{frame}.png')
                    img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                    temp_img_list.append(img)
                self.animation_list.append(temp_img_list)
        self.cls_frame_list = self.animation_list
        self.image = self.animation_list[self.action][self.frame_index]

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()

    def draw_fighter(self):
        """
        Method draws the created fighter on the screen.
        """
        self.rect.center = (self.x+self.offset, self.y)
        if self.tile_set:
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        if self.orientation == 'Right':
            self.screen.blit(self.image, self.rect)
        elif self.orientation == 'Left':
            self.screen.blit(pygame.transform.flip(self.image, True, False), self.rect)

    def update(self):
        """
        Method updates the animation of the fighter that's drawn on the screen.
        """
        animation_cooldown = 100
        # Handle animation
        # Update the image
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    @classmethod
    def get_frame_len(cls, action: int):
        return len(cls.cls_frame_list[action])

from screen import *
from screen import Screen


class Fighter(Screen):

    animations = {
        'Idle': 7,
        'Attack': 7,
        'Hurt': 2,
        'Death': 9
    }

    def __init__(self, x: float, y: int, offset: int, name: str, max_hp: int):
        super().__init__()
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0 - Idle, 1 - Attack, 2 - Hurt, 3 - Death
        self.update_time = pygame.time.get_ticks()
        self.x = x
        self.y = y
        self.offset = offset
        self.orientation = 'Right'
        # Load idle images
        for animation, count in self.animations.items():
            temp_img_list = []
            for frame in range(count):
                img = pygame.image.load(f'img/{self.name}/{animation}/{frame}.png')
                img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
                temp_img_list.append(img)
            self.animation_list.append(temp_img_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()

    def draw_fighter(self):
        self.rect.center = (self.x+self.offset, self.y)
        if self.orientation == 'Right':
            self.screen.blit(self.image, self.rect)
        elif self.orientation == 'Left':
            self.screen.blit(pygame.transform.flip(self.image, True, False), self.rect)

    def update(self):
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

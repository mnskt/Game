from pathlib import WindowsPath
import pygame


class ParseTileSet:
    def __init__(self, frame_height: int, img_folder_name: str):
        self.img_folder_name = img_folder_name
        self.frame_height = frame_height

    def create_frame_list(self):
        tile_set_idle_path = WindowsPath(f'img/{self.img_folder_name}/Idle/Idle.png')
        tile_set_run_path = WindowsPath(f'img/{self.img_folder_name}/Run/Run.png')
        tile_set_attack_path = WindowsPath(f'img/{self.img_folder_name}/Attack/Attack.png')
        tile_sets_paths = [tile_set_idle_path, tile_set_run_path, tile_set_attack_path]

        tile_set_idle = pygame.image.load(tile_set_idle_path).convert_alpha()
        tile_set_run = pygame.image.load(tile_set_run_path).convert_alpha()
        tile_set_attack = pygame.image.load(tile_set_attack_path).convert_alpha()

        no_of_frames_of_animations = {
            "Idle": (tile_set_idle, 4, 64),
            "Run": (tile_set_run, 8, 80),
            "Attack": (tile_set_attack, 8, 96)
        }
        all_frames = []

        for animation, data_set in no_of_frames_of_animations.items():
            temp_img_list = []
            for tile_set in tile_sets_paths:
                if animation == tile_set.stem:
                    for frame in range(data_set[1]):
                        frame = data_set[0].subsurface(pygame.Rect(
                            frame * data_set[2], 0, data_set[2], self.frame_height
                        ))
                        temp_img_list.append(frame)
                    all_frames.append(temp_img_list)
        return all_frames

    # Todo: for the future when tile set engine is required
    # def debug_create_frame_list(self):
    #     for tile_set in self.tile_set_path:
    #         self.tile_sets.append(pygame.image.load(tile_set).convert_alpha())
    #     for idx, tile_set in enumerate(self.tile_sets):
    #         for animation, count_width in self.no_of_frames_of_animations.items():
    #             temp_list = []
    #             if animation == self.tile_set_path[idx].stem:
    #                 for frame in range(count_width[0]):
    #                     frame = tile_set.subsurface(pygame.Rect(frame * count_width[1], 0, count_width[1],
    #                                                             self.frame_height))
    #                     temp_list.append(frame)
    #                 self.all_frames.append(temp_list)
    #     return self.all_frames

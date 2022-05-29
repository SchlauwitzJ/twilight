from __future__ import annotations
from typing import Union
from csv import reader
import pygame
from dataclasses import dataclass
from twilight.Sim_Visualizer.settings import *
import json
import os


def import_tile_unit_folder(path):
    surface_list = []

    for _, __, img_files in os.walk(path + '/animation'):
        for image in img_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (TILESIZE, TILESIZE))
            surface_list.append(image_surf)
    mat_icon = pygame.image.load(path + '/icon.png').convert_alpha()

    with open(path + '/data.json') as json_file:
        data = json.load(json_file)

    return surface_list, mat_icon, data


@dataclass
class ElementTile:
    """

    """

    def __init__(self, name='void', percent=1.0,
                 animation: Union[list[pygame.Surface((TILESIZE, TILESIZE))], None] = None,
                 icon=pygame.Surface((TILESIZE, TILESIZE)),
                 position: Union[list, tuple, None] = None, **kwargs):

        self.icon = icon

        if animation is None:
            self.animation = [pygame.Surface((TILESIZE, TILESIZE)).set_alpha(int(255 * self.percent))]
        else:
            self.animation = animation

        if kwargs is not None:
            self.data = kwargs

        self.data = {'position': position,
                     'image_index': 0,
                     'percent': percent,
                     'name': name}

    def rename(self, name: str):
        self.data['name'] = name
        return

    def create_variations(self, variations=1):
        compilation = []
        for _ in range(variations):
            full_path = f'./Visual_tiles/Materials/{self.data["name"]}'
            animation, icon, data = import_tile_unit_folder(full_path)

            # todo apply non uniform alpha to the tile
            compilation.append(ElementTile(name=self.data['name'],
                                           percent=self.data['percent'],
                                           animation=animation,
                                           icon=icon,
                                           data=data))

        return compilation

    def get_image(self):
        return self.animation[self.data['image_index']]

    def save_tile(self):
        if self.data['position'] is not None:
            full_path = './Visual_tiles/Loc'
            for coord in self.data['position']:
                full_path += '_' + str(int(coord))

            if not os.path.exists(full_path):
                os.mkdir(full_path)
        else:
            full_path = './Visual_tiles'

        full_path += f'/{self.data["name"]}'
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        # use the position first if it exists otherwise it is a generic tile

        with open(full_path + '/data.json', 'w') as fp:
            json.dump(self.data, fp, indent=4)
        pygame.image.save(self.icon, full_path + '/icon.png')

        if not os.path.exists(full_path + '/animation'):
            os.mkdir(full_path + '/animation')
        for ind, a_frame in enumerate(self.animation):
            pygame.image.save(a_frame, f'frame_{ind}.png')
        return

    def load_tile(self):
        if self.data['position'] is not None:
            full_path = './Visual_tiles/Loc'
            for coord in self.data['position']:
                full_path += '_' + str(int(coord))

            if not os.path.exists(full_path):
                # use a stereo-typical tile
                full_path = './Visual_tiles'
        else:
            # use a stereo-typical tile
            full_path = './Visual_tiles'

        full_path += f'/{self.data["name"]}'

        if not os.path.exists(full_path):
            os.mkdir(full_path)
            os.mkdir(full_path + '/animation')
            self.save_tile()
            raise ResourceWarning(f"Material tile {self.data['name']} in path: {full_path}"
                                  f" did not exist before (this warning will only show once)!")
        else:

            with open(full_path + '/data.json', 'w') as fp:
                self.data = json.load(fp)
            self.icon = pygame.image.load(full_path + '/icon.png').convert_alpha()

            self.animation = []
            for _, __, img_files in os.walk(full_path + '/animation'):
                for image in img_files:
                    frame_path = full_path + '/animation/' + image
                    image_surf = pygame.image.load(frame_path).convert_alpha()
                    image_surf = pygame.transform.scale(image_surf, (TILESIZE, TILESIZE))
                    self.animation.append(image_surf)
        return


if __name__ == '__main__':
    tile = ElementTile()

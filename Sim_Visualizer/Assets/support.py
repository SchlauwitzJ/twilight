from csv import reader
from os import walk
import pygame


def import_csv_layout(path: str) -> list:
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            # todo remove this when all images are correctly scaled
            image_surf = pygame.transform.scale(image_surf, (64, 64))
            surface_list.append(image_surf)

    return surface_list


# print(import_csv_layout('../graphics/maps/Export/test_map_Rocks.csv'))

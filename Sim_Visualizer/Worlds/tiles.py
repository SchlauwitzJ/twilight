from __future__ import annotations
from typing import Union
import pygame
from ..settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_type, groups: list,
                 surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)

        self.image = surface
        self.sprite_type = sprite_type
        # self.image = pygame.image.load('./graphics/terrain/rock_01.png').convert_alpha()
        # self.image = pygame.transform.scale(self.image, (64, 64))
        if sprite_type == 'object':
            # do an offset
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)  # less 5 pixels on top and bottom

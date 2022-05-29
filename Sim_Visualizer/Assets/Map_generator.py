from __future__ import annotations

import copy
from typing import Union
from dataclasses import dataclass
import random
import numpy as np
import time
import sys
from matplotlib import pyplot as plt


@dataclass
class TileUnit:
    structure = {}
    is_inverted = False


def euclidean(vec1, vec2):
    return np.sqrt((vec1[0]-vec2[0])**2 + (vec1[1]-vec2[1])**2)


class Dijkstra:
    def __init__(self, size_xy: Union[tuple, list],
                 seed: Union[int, None] = None,
                 loop_dims: Union[list, bool] = False,
                 cell_count=2):
        self.r_seed = seed
        self.cell_count = cell_count
        self.map_size = size_xy

        if not loop_dims:
            self.loop_dims = []
        elif isinstance(loop_dims, list):
            self.loop_dims = loop_dims
        else:
            self.loop_dims = list(range(len(self.map_size)))

        if seed is not None:
            self.r_seed = seed
        else:
            self.r_seed = random.randrange(2**32-1)

        # plate/region maps
        self.plate_map = -np.ones(size_xy, dtype=int)
        self.weight_map = np.ones(size_xy, dtype=int) * np.infty
        self.plate_points = []
        self.plate_pool = []

        # gradient related maps
        self.height_map = np.zeros(size_xy, dtype=int)

    def get_seed(self):
        return self.r_seed

    def generate_groups(self):
        """
        thickness reach: relative to the neighboring plates, determines which plate a tile belongs to.
        thickness means: equate to the relative thickness and mass of the plate
        :return:
        """

        self.plate_pool = []
        for plate_num in range(self.cell_count):
            # plate center position
            x_ind = np.random.randint(0, self.map_size[0])
            y_ind = np.random.randint(0, self.map_size[1])

            self.plate_map[x_ind][y_ind] = plate_num
            self.weight_map[x_ind][y_ind] = 0
            self.plate_points.append((x_ind, y_ind))
            self.plate_pool.append((x_ind, y_ind))

        return

    def generate_neighbors(self, pos: int, axis=0) -> list:
        rang = [pos - 1, pos, pos + 1]
        if pos <= 0:
            if axis in self.loop_dims:
                rang[0] %= self.map_size[axis]
            else:
                rang.pop(0)
        if pos >= self.map_size[axis] - 1:
            if axis in self.loop_dims:
                rang[-1] %= self.map_size[axis]
            else:
                rang.pop(-1)

        return rang

    def eval_neighbors(self, pos) -> list:
        x_rang = self.generate_neighbors(pos=pos[0], axis=0)
        y_rang = self.generate_neighbors(pos=pos[1], axis=1)

        ref_plate = self.plate_map[pos[0]][pos[1]]
        centroid = self.plate_points[ref_plate]
        new_group = []
        for x_ind in x_rang:
            for y_ind in y_rang:
                plate_id = self.plate_map[x_ind][y_ind]
                pos_weight = euclidean(centroid, (x_ind, y_ind))
                if plate_id == -1:
                    self.plate_map[x_ind][y_ind] = ref_plate
                    self.weight_map[x_ind][y_ind] = pos_weight
                    new_group.append((x_ind, y_ind))
                elif self.weight_map[x_ind][y_ind] > pos_weight:
                    self.plate_map[x_ind][y_ind] = ref_plate
                    self.weight_map[x_ind][y_ind] = pos_weight
                    new_group.append((x_ind, y_ind))

        return new_group

    # map population methods
    def fill(self):
        # allow for repeatability if a seed is given
        print(self.r_seed)
        np.random.seed(self.r_seed)

        # generate centroids
        self.generate_groups()
        active_points = self.plate_points
        while len(active_points):
            new_points = []
            for plate_point in active_points:
                new_points += self.eval_neighbors(pos=plate_point)

            active_points = new_points
        return

    # display the first layer of the map
    def show_map(self):
        plt.imshow(self.plate_map, interpolation='nearest')
        plt.show()
        plt.imshow(self.weight_map, interpolation='nearest')
        plt.show()
        return


class MapGenerator:
    def __init__(self, size_xyz: Union[tuple, list],
                 seed: Union[int, None] = None,
                 loop_dims: Union[list, bool] = False,
                 fill_percent=0.1):
        self.r_seed = seed
        self.fill_percent = fill_percent
        self.map_size = size_xyz
        self.number_map = -np.ones(size_xyz, dtype=int)
        self.tile_map = self.generate_tile_map(self.map_size)

        if not loop_dims:
            self.loop_dims = []
        elif isinstance(loop_dims, list):
            self.loop_dims = loop_dims
        else:
            self.loop_dims = list(range(len(self.map_size)))

        if seed is not None:
            self.r_seed = seed
        else:
            self.r_seed = random.randrange(sys.maxsize)

    def get_seed(self):
        return self.r_seed

    def generate_tile_map(self, dims: list):
        tile_row = []
        if len(dims) > 1:
            for _ in range(dims[0]):
                tile_row.append(self.generate_tile_map(dims=dims[1:]))
        else:
            for _ in range(dims[0]):
                tile_row.append(TileUnit())

        return tile_row

    # map population methods
    def random_fill(self):
        random.seed(self.r_seed)
        for x_ind in range(self.map_size[0]):
            for y_ind in range(self.map_size[1]):
                for z_ind in range(self.map_size[2]):
                    self.number_map[x_ind][y_ind][z_ind] = np.random.rand() < self.fill_percent

    # display the first layer of the map
    def show_map(self):
        plt.imshow(self.number_map[0], interpolation='nearest')
        plt.show()
        return


if __name__ == '__main__':
    mg = Dijkstra(size_xy=(256, 256), cell_count=5, seed=1000, loop_dims=True)
    # mg = Dijkstra(size_xy=(256, 256), cell_count=5, loop_dims=True)
    mg.fill()
    mg.show_map()

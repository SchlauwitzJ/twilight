import pygame
import sys

from twilight.Sim_Visualizer.Worlds.D2_world import World
from twilight.Sim_Visualizer.settings import *


class Sim:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("DnD")
        self.clock = pygame.time.Clock()
        self.world = World()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('brown')
            self.world.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    sim = Sim()
    sim.run()

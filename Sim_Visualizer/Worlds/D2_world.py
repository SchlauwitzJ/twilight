import pygame
from twilight.Sim_Visualizer.settings import *
from twilight.Sim_Visualizer.Worlds.tiles import Tile
from twilight.Sim_Visualizer.Worlds.agents import Agent
from twilight.Sim_Visualizer.Worlds.tools import Item
from twilight.Sim_Visualizer.visual_debug import debug
from twilight.Sim_Visualizer.Assets.Groups import YSortCameraGroup
from twilight.Sim_Visualizer.Assets.support import import_csv_layout, import_folder
from twilight.Sim_Visualizer.Assets.ui import UI
from twilight.Sim_Visualizer.Worlds.NPCs import Enemy
import random


class World:
    def __init__(self):
        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.player = None

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        layouts = {"boundary": import_csv_layout('./graphics/maps/Export/test_map_Rocks.csv'),
                   "grass": import_csv_layout('./graphics/maps/Export/test_map_cliffs.csv'),
                   "object": import_csv_layout('./graphics/maps/Export/test_map_Entities.csv'),
                   "entities": import_csv_layout('./graphics/maps/Export/test_map_Entities.csv')}

        graphics = {
            'grass': import_folder('./graphics/terrain'),
            'object': import_folder('./graphics/Entities')
        }

        for style, layout in layouts.items():
            for latitude, lat_slice in enumerate(layout):
                for longitude, lat_lon in enumerate(lat_slice):
                    if lat_lon != '-1':
                        x = longitude * TILESIZE
                        y = latitude * TILESIZE
                        if style == 'boundary':
                            Tile(pos=(x, y), groups=[self.obstacle_sprites],
                                 sprite_type="invisible")
                        elif style == 'grass':
                            random_grass_image = random.choice(graphics['grass'])
                            Tile(pos=(x, y), groups=[self.visible_sprites,
                                                     self.attackable_sprites,
                                                     self.obstacle_sprites],
                                 sprite_type="grass", surface=random_grass_image)
                        elif style == 'object':
                            # todo separate pixel arts into separte image files
                            # obj_surf = graphics['object'][int(lat_lon)]
                            obj_surf = graphics['object'][0]
                            Tile(pos=(x, y), groups=[self.visible_sprites,
                                                     self.obstacle_sprites],
                                 sprite_type="object", surface=obj_surf)
                        elif style == 'entities':
                            if lat_lon == '8':
                                self.player = Agent(pos=(x, y), groups=[self.visible_sprites],
                                                    obstacle_sprites=self.obstacle_sprites,
                                                    create_attack=self.create_attack,
                                                    destroy_attack=self.destroy_attack,
                                                    create_magic=self.create_magic,
                                                    destroy_magic=self.destroy_magic)
                            else:
                                if lat_lon == '1':
                                    monster_name = 'squid'
                                elif lat_lon == '2':
                                    monster_name = 'bamboo'
                                elif lat_lon == '3':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'spirit'

                                Enemy(monster_name, (x, y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      obstacle_sprites=self.obstacle_sprites,
                                      damage_player=self.damage_player)

    def create_attack(self):
        self.current_attack = Item(agent=self.player, groups=[self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
        return

    def create_magic(self, style, strength, cost):
        print(style, strength, cost)

    def destroy_magic(self):
        return

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
        return

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # spawn particle effects
        return

    def run(self):
        # update the world
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

        # debug(self.player.status)
        # debug(self.player.direction)
        return

import pygame
from twilight.Sim_Visualizer.settings import *
from twilight.Sim_Visualizer.Assets.support import import_folder
from twilight.Sim_Visualizer.Assets.Entities import Entity
from twilight.Sim_Visualizer.visual_debug import debug


class Agent(Entity):
    def __init__(self, pos, groups: list, obstacle_sprites,
                 create_attack, destroy_attack,
                 create_magic, destroy_magic):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/Entities/red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)  # less 13 pixels on top and bottom

        # graphics setup
        self.animations = {}
        self.import_assets()
        self.status = 'down'

        # movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic
        self.create_magic = create_magic
        self.destroy_magic = destroy_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health'] * 0.6
        self.energy = self.stats['energy'] * 0.9
        self.exp = 123
        self.speed = self.stats['speed']

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # external stuff
        self.obstacle_sprites = obstacle_sprites

    def import_assets(self):
        agent_path = './graphics/Entities'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []
                           }
        for animation in self.animations.keys():
            # todo separate assets by direction and action
            full_path = agent_path + '/' + animation
            self.animations[animation] = import_folder(full_path)
        return

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement input
            self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]

            if self.direction.y < 0:
                self.status = 'up'
            elif self.direction.y > 0:
                self.status = 'down'
            # favor left-right frames over up-down frames
            if self.direction.x < 0:
                self.status = 'left'
            elif self.direction.x > 0:
                self.status = 'right'

            # attack input
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # magic input
            if keys[pygame.K_LCTRL] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                weapon_list = list(weapon_data.keys())
                if self.weapon_index < len(weapon_list) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = weapon_list[self.weapon_index]

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                magic_list = list(magic_data.keys())
                if self.magic_index < len(magic_list) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = magic_list[self.magic_index]

        return

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.y = 0
            self.direction.x = 0
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        elif 'attack' in self.status:
            self.status = self.status.replace('_attack', '')

        return

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
        return

    def animate(self):
        animation = self.animations[self.status]
        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        # set the image
        self.image = animation[0]
        # todo enable this when images are split
        # self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            # flicker
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        return

    def update(self) -> None:
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)

import pygame
from twilight.Sim_Visualizer.settings import *
from twilight.Sim_Visualizer.Assets.Entities import Entity
from twilight.Sim_Visualizer.Assets.support import import_folder


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player):
        # general setup
        super().__init__(groups=groups)
        self.sprite_type = 'enemy'

        # movement
        self.status = 'idle'

        # graphics setup
        self.animations = {}
        self.import_graphics(monster_name)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # external
        self.obstacle_sprites = obstacle_sprites

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown_time = 400
        self.damage_player = damage_player

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'./graphics/Monsters/'
        # main_path = f'./graphics/Monsters/{name}/' todo
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
        return

    def get_agent_distance_direction(self, agent):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        agent_vec = pygame.math.Vector2(agent.rect.center)

        direction = agent_vec - enemy_vec
        distance = direction.magnitude()

        if distance > 0:
            direction = direction.normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, agent):
        distance = self.get_agent_distance_direction(agent)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

        return

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_agent_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                # magic damage
                pass
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= - self.resistance
        return

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def actions(self, agent):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_agent_distance_direction(agent)[1]
        else:
            self.direction = pygame.math.Vector2()
        return

    def animate(self):
        animation = self.animations[self.status]
        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
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

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown_time:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

        return

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.check_death()
        self.cooldowns()

    def enemy_update(self, agent):
        self.get_status(agent)
        self.actions(agent)


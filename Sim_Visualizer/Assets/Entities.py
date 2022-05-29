import pygame
from math import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups: list):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision(direction="horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision(direction="vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """
        assuming static collisions
        :param direction:
        :return:
        """
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        # moving right -> snap to obstacle left side
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        # moving left -> snap to obstacle right side
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        # moving down -> snap to obstacle top side
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        # moving up -> snap to obstacle bottom side
                        self.hitbox.top = sprite.hitbox.bottom
        return

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        return 0

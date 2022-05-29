import pygame


class Item(pygame.sprite.Sprite):
    def __init__(self, agent, groups: list):
        super().__init__(groups)
        direction = agent.status.split('_')[0]
        # print('attack ', direction)
        self.sprite_type = 'weapon'

        # graphic
        full_path = f'./graphics/Weapons/{agent.weapon}/{direction}.png'

        self.image = pygame.image.load(full_path).convert_alpha()
        # todo remove this when ready
        self.image = pygame.transform.scale(self.image, (64, 64))

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft=agent.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright=agent.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop=agent.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom=agent.rect.midtop + pygame.math.Vector2(-10, 0))

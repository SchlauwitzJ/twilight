import pygame
from twilight.Sim_Visualizer.settings import *


class UI:
    def __init__(self):
        # general info
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, BAR_HEIGHT + 2*10,
                                           ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            weapon = pygame.image.load(weapon['graphic']).convert_alpha()
            # todo remove this when ready
            weapon = pygame.transform.scale(weapon, (64, 64))
            self.weapon_graphics.append(weapon)

        # convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            # todo remove this when ready
            magic = pygame.transform.scale(magic, (64, 64))
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # convert stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # draw the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)
        self.display_surface.blit(text_surf, text_rect)
        return

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)

        weapon_surf = self.weapon_graphics[weapon_index]
        # weapon_surf = self.weapon_graphics[0]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)
        return

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(80, 640, has_switched)
        # todo
        # magic_surf = self.magic_graphics[magic_index]
        magic_surf = self.magic_graphics[0]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)
        return

    def display(self, agent):
        self.show_bar(agent.health, agent.stats['health'],
                      self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(agent.energy, agent.stats['energy'],
                      self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(agent.exp)
        self.weapon_overlay(agent.weapon_index, not agent.can_switch_weapon)
        self.magic_overlay(agent.magic_index, not agent.can_switch_magic)
        return


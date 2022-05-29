"""
Setup
Font Sources:
    https://www.dafont.com/theme.php?cat=114
Audio Sources:
    https://opengameart.org/content/rpg-sound-pack
Graphic Sources:

"""
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = './graphics/Fonts/D_Day_Stencil.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#eeeeee'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# weapons
weapon_data = {'sword': {'cooldown': 100, 'damage': 15, 'graphic': './graphics/Solid_color_tiles/red.png'},
               'lance': {'cooldown': 400, 'damage': 30, 'graphic': './graphics/Solid_color_tiles/red.png'},
               'axe': {'cooldown': 300, 'damage': 20, 'graphic': './graphics/Solid_color_tiles/red.png'},
               'rapier': {'cooldown': 50, 'damage': 5, 'graphic': './graphics/Solid_color_tiles/red.png'},
               'sai': {'cooldown': 80, 'damage': 10, 'graphic': './graphics/Solid_color_tiles/red.png'}}

# magic
magic_data = {'flame': {'strength': 5, 'cost': 20, 'graphic': './graphics/Solid_color_tiles/dark_red.png'},
              'heal': {'strength': 20, 'cost': 10, 'graphic': './graphics/Solid_color_tiles/dark_red.png'},
              }

# enemy data
monster_data = {'squid': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash',
                          'attack_sound': './audio/battle/swing.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80,
                          'notice_radius': 360},
                'raccoon': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash',
                            'attack_sound': './audio/battle/swing.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80,
                            'notice_radius': 360},
                'spirit': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash',
                           'attack_sound': './audio/battle/swing.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80,
                           'notice_radius': 360},
                'bamboo': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash',
                           'attack_sound': './audio/battle/swing.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80,
                           'notice_radius': 360},
                }

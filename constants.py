WALL = -1
EMPTY = 0
TARGET = 1
BOX = 2
PLAYER = 3
BOX_ON_TARGET = 4
PLAYER_ON_TARGET = 5

CELL_SIZE = 64
SPRITE_SIZE = 16

WINDOW_TITLE = "Auto Sokoban"

UI_BAR_HEIGHT = 60
BTN_COLOR         = (101, 67, 33)
BTN_HOVER_COLOR   = (139, 90, 43)
BTN_TEXT_COLOR    = (255, 240, 200)
UI_BG_COLOR       = (62, 45, 25)

# Positions des sprites dans les spritesheets (fichier, x, y)
SPRITE_FLOOR     = ("assets/tileset_farm.png",  0,   0)
SPRITE_WALL      = ("assets/tileset_farm.png",  64,  16)
SPRITE_BOX       = ("assets/crates.png",        0,   0)

SPRITE_PLAYER_DOWN  = ("assets/character.png", 752, 128)
SPRITE_PLAYER_UP    = ("assets/character.png", 752, 96)
SPRITE_PLAYER_LEFT  = ("assets/character.png", 736, 112)
SPRITE_PLAYER_RIGHT = ("assets/character.png", 768, 112)

# Directions
DOWN  = "down"
UP    = "up"
LEFT  = "left"
RIGHT = "right"

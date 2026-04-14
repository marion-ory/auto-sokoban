import pygame
from constants import *

def load_sprite(filepath, x, y):
    sheet = pygame.image.load(filepath).convert_alpha()
    tile = sheet.subsurface((x, y, SPRITE_SIZE, SPRITE_SIZE))
    return pygame.transform.scale(tile, (CELL_SIZE, CELL_SIZE))

def load_sprites():
    sprites = {}
    sprites[EMPTY]          = load_sprite(*SPRITE_FLOOR)
    sprites[TARGET]         = load_sprite(*SPRITE_FLOOR)
    sprites[WALL]           = load_sprite(*SPRITE_WALL)
    sprites[BOX]            = load_sprite(*SPRITE_BOX)
    sprites[BOX_ON_TARGET]  = load_sprite(*SPRITE_BOX)
    sprites[PLAYER]         = load_sprite(*SPRITE_PLAYER)
    sprites[PLAYER_ON_TARGET] = load_sprite(*SPRITE_PLAYER)
    return sprites

def draw_target_marker(surface, x, y):
    margin = CELL_SIZE // 4
    color = (180, 120, 50)
    thickness = 3
    pygame.draw.line(surface, color,
                     (x + margin, y + margin),
                     (x + CELL_SIZE - margin, y + CELL_SIZE - margin), thickness)
    pygame.draw.line(surface, color,
                     (x + CELL_SIZE - margin, y + margin),
                     (x + margin, y + CELL_SIZE - margin), thickness)

def draw_grid(surface, grid, sprites):
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            x = col_idx * CELL_SIZE
            y = row_idx * CELL_SIZE

            surface.blit(sprites[EMPTY], (x, y))

            if cell == WALL:
                surface.blit(sprites[WALL], (x, y))
            elif cell == TARGET:
                draw_target_marker(surface, x, y)
            elif cell == BOX:
                surface.blit(sprites[BOX], (x, y))
            elif cell == BOX_ON_TARGET:
                surface.blit(sprites[BOX_ON_TARGET], (x, y))
                draw_target_marker(surface, x, y)
            elif cell == PLAYER:
                surface.blit(sprites[PLAYER], (x, y))
            elif cell == PLAYER_ON_TARGET:
                draw_target_marker(surface, x, y)
                surface.blit(sprites[PLAYER], (x, y))

def init_display(grid):
    pygame.init()
    rows = len(grid)
    cols = len(grid[0])
    width = cols * CELL_SIZE
    height = rows * CELL_SIZE
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption(WINDOW_TITLE)
    sprites = load_sprites()
    return surface, sprites

import pygame
from constants import *

def load_sprite(filepath, x, y):
    sheet = pygame.image.load(filepath).convert_alpha()
    tile = sheet.subsurface((x, y, SPRITE_SIZE, SPRITE_SIZE))
    return pygame.transform.scale(tile, (CELL_SIZE, CELL_SIZE))

def load_sprites():
    sprites = {}
    sprites[EMPTY]            = load_sprite(*SPRITE_FLOOR)
    sprites[WALL]             = load_sprite(*SPRITE_WALL)
    sprites[BOX]              = load_sprite(*SPRITE_BOX)
    sprites[BOX_ON_TARGET]    = load_sprite(*SPRITE_BOX)
    sprites["player_down"]    = load_sprite(*SPRITE_PLAYER_DOWN)
    sprites["player_up"]      = load_sprite(*SPRITE_PLAYER_UP)
    sprites["player_left"]    = load_sprite(*SPRITE_PLAYER_LEFT)
    sprites["player_right"]   = load_sprite(*SPRITE_PLAYER_RIGHT)
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

def draw_grid(surface, grid, sprites, direction=DOWN):
    player_sprite = sprites[f"player_{direction}"]

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
                surface.blit(player_sprite, (x, y))
            elif cell == PLAYER_ON_TARGET:
                draw_target_marker(surface, x, y)
                surface.blit(player_sprite, (x, y))

def draw_button(surface, rect, text, font, hovered=False):
    color = BTN_HOVER_COLOR if hovered else BTN_COLOR
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, BTN_TEXT_COLOR, rect, 2, border_radius=8)
    label = font.render(text, True, BTN_TEXT_COLOR)
    lx = rect.x + (rect.width - label.get_width()) // 2
    ly = rect.y + (rect.height - label.get_height()) // 2
    surface.blit(label, (lx, ly))

def draw_ui(surface, font, buttons, mouse_pos, moves):
    win_width = surface.get_width()
    grid_height = surface.get_height() - UI_BAR_HEIGHT

    pygame.draw.rect(surface, UI_BG_COLOR, (0, grid_height, win_width, UI_BAR_HEIGHT))

    moves_text = font.render(f"Coups : {moves}", True, BTN_TEXT_COLOR)
    surface.blit(moves_text, (12, grid_height + (UI_BAR_HEIGHT - moves_text.get_height()) // 2))

    for name, rect in buttons.items():
        hovered = rect.collidepoint(mouse_pos)
        label = "Annuler" if name == "undo" else "Reset"
        draw_button(surface, rect, label, font, hovered)

def make_buttons(win_width, grid_height):
    btn_w, btn_h = 110, 36
    margin = 12
    y = grid_height + (UI_BAR_HEIGHT - btn_h) // 2
    undo_rect  = pygame.Rect(win_width - 2 * (btn_w + margin), y, btn_w, btn_h)
    reset_rect = pygame.Rect(win_width - (btn_w + margin),     y, btn_w, btn_h)
    return {"undo": undo_rect, "reset": reset_rect}

def init_display(grid):
    pygame.init()
    rows = len(grid)
    cols = len(grid[0])
    width  = cols * CELL_SIZE
    height = rows * CELL_SIZE + UI_BAR_HEIGHT
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption(WINDOW_TITLE)
    sprites = load_sprites()
    font = pygame.font.SysFont("Arial", 18, bold=True)
    buttons = make_buttons(width, rows * CELL_SIZE)
    return surface, sprites, font, buttons

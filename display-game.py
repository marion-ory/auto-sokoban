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

    labels = {"quit": "Quitter", "undo": "Annuler", "reset": "Reset"}
    for name, rect in buttons.items():
        draw_button(surface, rect, labels[name], font, rect.collidepoint(mouse_pos))

def make_buttons(win_width, grid_height):
    btn_w, btn_h = 90, 34
    margin = 8
    y = grid_height + (UI_BAR_HEIGHT - btn_h) // 2
    quit_rect  = pygame.Rect(win_width - 3 * (btn_w + margin), y, btn_w, btn_h)
    undo_rect  = pygame.Rect(win_width - 2 * (btn_w + margin), y, btn_w, btn_h)
    reset_rect = pygame.Rect(win_width - (btn_w + margin),     y, btn_w, btn_h)
    return {"quit": quit_rect, "undo": undo_rect, "reset": reset_rect}

def draw_menu(surface, font_title, font_btn, mouse_pos):
    surface.fill(MENU_BG_COLOR)

    # Herbe décorative en fond (tuiles répétées)
    cols = surface.get_width() // CELL_SIZE + 1
    rows = surface.get_height() // CELL_SIZE + 1

    # Titre
    shadow = font_title.render("Auto Sokoban", True, MENU_SHADOW_COLOR)
    title  = font_title.render("Auto Sokoban", True, MENU_TITLE_COLOR)
    tx = (surface.get_width() - title.get_width()) // 2
    ty = surface.get_height() // 5
    surface.blit(shadow, (tx + 3, ty + 3))
    surface.blit(title,  (tx, ty))

    # Sous-titre
    sub = font_btn.render("Un puzzle cozy à résoudre !", True, MENU_TITLE_COLOR)
    surface.blit(sub, ((surface.get_width() - sub.get_width()) // 2, ty + title.get_height() + 10))

    # Boutons du menu
    btn_w, btn_h = 200, 50
    cx = (surface.get_width() - btn_w) // 2
    play_rect = pygame.Rect(cx, surface.get_height() // 2,      btn_w, btn_h)
    quit_rect = pygame.Rect(cx, surface.get_height() // 2 + 70, btn_w, btn_h)

    draw_button(surface, play_rect, "Jouer",  font_btn, play_rect.collidepoint(mouse_pos))
    draw_button(surface, quit_rect, "Quitter", font_btn, quit_rect.collidepoint(mouse_pos))

    return {"play": play_rect, "quit": quit_rect}

def init_display(grid):
    pygame.init()
    rows = len(grid)
    cols = len(grid[0])
    width  = max(cols * CELL_SIZE, MENU_WIDTH)
    height = rows * CELL_SIZE + UI_BAR_HEIGHT
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption(WINDOW_TITLE)
    sprites    = load_sprites()
    font       = pygame.font.SysFont("Arial", 18, bold=True)
    font_title = pygame.font.SysFont("Arial", 52, bold=True)
    buttons    = make_buttons(width, rows * CELL_SIZE)
    return surface, sprites, font, font_title, buttons

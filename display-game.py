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
    color = (220, 40, 40)
    thickness = 4
    pygame.draw.line(surface, color,
                     (x + margin, y + margin),
                     (x + CELL_SIZE - margin, y + CELL_SIZE - margin), thickness)
    pygame.draw.line(surface, color,
                     (x + CELL_SIZE - margin, y + margin),
                     (x + margin, y + CELL_SIZE - margin), thickness)

def draw_grid(surface, grid, sprites, direction=DOWN):
    player_sprite = sprites[f"player_{direction}"]

    win_w  = surface.get_width()
    grid_w = len(grid[0]) * CELL_SIZE
    grid_h = len(grid)    * CELL_SIZE
    offset_x = (win_w - grid_w) // 2

    # Fond herbe sur toute la surface de jeu
    for gy in range(0, grid_h, CELL_SIZE):
        for gx in range(0, win_w, CELL_SIZE):
            surface.blit(sprites[EMPTY], (gx, gy))

    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            x = offset_x + col_idx * CELL_SIZE
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

def draw_level_select(surface, font_title, font_btn, mouse_pos, levels, page=0, filter_diff="Tous"):
    surface.fill(MENU_BG_COLOR)
    w = surface.get_width()
    buttons = {}

    # Titre
    title  = font_title.render("Choisir un niveau", True, MENU_TITLE_COLOR)
    shadow = font_title.render("Choisir un niveau", True, MENU_SHADOW_COLOR)
    tx = (w - title.get_width()) // 2
    surface.blit(shadow, (tx + 3, 18))
    surface.blit(title,  (tx, 15))

    # ── Filtres par difficulté ──
    filter_y   = 80
    filter_w   = 100
    filter_gap = 12
    total_fw   = len(DIFFICULTIES) * filter_w + (len(DIFFICULTIES) - 1) * filter_gap
    filter_x0  = (w - total_fw) // 2

    for j, diff in enumerate(DIFFICULTIES):
        fx   = filter_x0 + j * (filter_w + filter_gap)
        rect = pygame.Rect(fx, filter_y, filter_w, 34)
        active = (diff == filter_diff)
        color  = DIFF_COLORS.get(diff, BTN_COLOR) if active else BTN_COLOR
        if rect.collidepoint(mouse_pos) and not active:
            color = BTN_HOVER_COLOR
        pygame.draw.rect(surface, color, rect, border_radius=6)
        pygame.draw.rect(surface, BTN_TEXT_COLOR, rect, 2, border_radius=6)
        lbl = font_btn.render(diff, True, BTN_TEXT_COLOR)
        surface.blit(lbl, (rect.x + (filter_w - lbl.get_width()) // 2,
                           rect.y + (34 - lbl.get_height()) // 2))
        buttons[f"filter_{diff}"] = rect

    # ── Filtrer les niveaux ──
    filtered = [(i, lv) for i, lv in enumerate(levels)
                if filter_diff == "Tous" or lv["difficulty"] == filter_diff]

    total_pages = max(1, (len(filtered) + LEVELS_PER_PAGE - 1) // LEVELS_PER_PAGE)
    page        = max(0, min(page, total_pages - 1))

    start   = page * LEVELS_PER_PAGE
    visible = filtered[start:start + LEVELS_PER_PAGE]

    # ── Boutons de niveaux ──
    btn_w, btn_h = 300, 46
    cx      = (w - btn_w) // 2
    start_y = 130
    spacing = 54

    for slot, (real_idx, level) in enumerate(visible):
        rect   = pygame.Rect(cx, start_y + slot * spacing, btn_w, btn_h)
        hovered = rect.collidepoint(mouse_pos)
        pygame.draw.rect(surface, BTN_HOVER_COLOR if hovered else BTN_COLOR, rect, border_radius=8)
        pygame.draw.rect(surface, BTN_TEXT_COLOR, rect, 2, border_radius=8)

        name_surf = font_btn.render(level["name"], True, BTN_TEXT_COLOR)
        surface.blit(name_surf, (rect.x + 14, rect.y + (btn_h - name_surf.get_height()) // 2))

        diff_color = DIFF_COLORS.get(level["difficulty"], BTN_TEXT_COLOR)
        diff_surf  = font_btn.render(level["difficulty"], True, diff_color)
        surface.blit(diff_surf, (rect.right - diff_surf.get_width() - 14,
                                  rect.y + (btn_h - diff_surf.get_height()) // 2))
        buttons[f"level_{slot}"] = (rect, real_idx)

    # ── Pagination ──
    nav_y   = start_y + LEVELS_PER_PAGE * spacing + 8
    nav_w   = 110
    prev_rect = pygame.Rect(cx,              nav_y, nav_w, 38)
    next_rect = pygame.Rect(cx + btn_w - nav_w, nav_y, nav_w, 38)
    back_rect = pygame.Rect(cx + (btn_w - nav_w) // 2, nav_y, nav_w, 38)

    if page > 0:
        draw_button(surface, prev_rect, "◀ Préc.", font_btn, prev_rect.collidepoint(mouse_pos))
        buttons["prev"] = prev_rect

    if page < total_pages - 1:
        draw_button(surface, next_rect, "Suiv. ▶", font_btn, next_rect.collidepoint(mouse_pos))
        buttons["next"] = next_rect

    draw_button(surface, back_rect, "Retour", font_btn, back_rect.collidepoint(mouse_pos))
    buttons["back"] = back_rect

    # ── Indicateur de page ──
    page_txt = font_btn.render(f"{page + 1} / {total_pages}", True, MENU_TITLE_COLOR)
    surface.blit(page_txt, ((w - page_txt.get_width()) // 2, nav_y + 46))

    return buttons

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

MIN_GAME_WIDTH = 3 * (90 + 8) + 160  # 3 boutons + marge + texte "Coups :"

def resize_display(grid):
    rows = len(grid)
    cols = len(grid[0])
    width  = max(cols * CELL_SIZE, MIN_GAME_WIDTH)
    height = rows * CELL_SIZE + UI_BAR_HEIGHT
    surface = pygame.display.set_mode((width, height))
    buttons = make_buttons(width, rows * CELL_SIZE)
    return surface, buttons

def resize_to_menu(surface):
    if surface.get_width() != MENU_WIDTH or surface.get_height() != MENU_HEIGHT:
        return pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    return surface

def init_display(grid):
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)
    surface, buttons = resize_display(grid)
    sprites    = load_sprites()
    font       = pygame.font.SysFont("Arial", 18, bold=True)
    font_title = pygame.font.SysFont("Arial", 52, bold=True)
    return surface, sprites, font, font_title, buttons

import pygame
import importlib
display_game = importlib.import_module("display-game")
from constants import *
from levels import get_level, level_count, LEVELS

def find_player(grid):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == PLAYER or cell == PLAYER_ON_TARGET:
                return r, c
    return None

def move_player(grid, dr, dc):
    pos = find_player(grid)
    if pos is None:
        return grid

    r, c = pos
    nr, nc = r + dr, c + dc

    if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0])):
        return grid
    if grid[nr][nc] == WALL:
        return grid

    new_grid = [row[:] for row in grid]
    target_cell = grid[nr][nc]

    if target_cell == BOX or target_cell == BOX_ON_TARGET:
        br, bc = nr + dr, nc + dc
        if not (0 <= br < len(grid) and 0 <= bc < len(grid[0])):
            return grid
        if grid[br][bc] == WALL or grid[br][bc] == BOX or grid[br][bc] == BOX_ON_TARGET:
            return grid
        new_grid[br][bc] = BOX_ON_TARGET if grid[br][bc] == TARGET else BOX

    new_grid[nr][nc] = PLAYER_ON_TARGET if (target_cell == TARGET or target_cell == BOX_ON_TARGET) else PLAYER
    new_grid[r][c] = TARGET if grid[r][c] == PLAYER_ON_TARGET else EMPTY

    return new_grid

def is_won(grid):
    for row in grid:
        if BOX in row:
            return False
    return True

def load_level(index):
    grid, name, difficulty = get_level(index)
    return grid, name, difficulty, DOWN, [], 0

def main():
    current_level = 0
    grid, level_name, difficulty, direction, history, moves = load_level(current_level)
    state       = STATE_MENU
    select_page = 0
    select_diff = "Tous"

    surface, sprites, font, font_title, buttons = display_game.init_display(grid)
    clock   = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu_btns = display_game.draw_menu(surface, font_title, font, mouse_pos)
                    if menu_btns["play"].collidepoint(mouse_pos):
                        surface = display_game.resize_to_menu(surface)
                        state = STATE_SELECT
                    elif menu_btns["quit"].collidepoint(mouse_pos):
                        running = False

            elif state == STATE_SELECT:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sel_btns = display_game.draw_level_select(
                        surface, font_title, font, mouse_pos,
                        LEVELS, select_page, select_diff
                    )

                    # Filtres
                    for diff in DIFFICULTIES:
                        if f"filter_{diff}" in sel_btns and sel_btns[f"filter_{diff}"].collidepoint(mouse_pos):
                            select_diff = diff
                            select_page = 0

                    # Niveaux
                    for slot in range(LEVELS_PER_PAGE):
                        key = f"level_{slot}"
                        if key in sel_btns:
                            rect, real_idx = sel_btns[key]
                            if rect.collidepoint(mouse_pos):
                                current_level = real_idx
                                grid, level_name, difficulty, direction, history, moves = load_level(current_level)
                                surface, buttons = display_game.resize_display(grid)
                                state = STATE_PLAYING

                    # Pagination
                    if "prev" in sel_btns and sel_btns["prev"].collidepoint(mouse_pos):
                        select_page -= 1
                    if "next" in sel_btns and sel_btns["next"].collidepoint(mouse_pos):
                        select_page += 1
                    if "back" in sel_btns and sel_btns["back"].collidepoint(mouse_pos):
                        surface = display_game.resize_to_menu(surface)
                        state = STATE_MENU

            elif state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    new_grid = grid
                    if event.key == pygame.K_DOWN:
                        direction = DOWN
                        new_grid = move_player(grid, 1, 0)
                    elif event.key == pygame.K_UP:
                        direction = UP
                        new_grid = move_player(grid, -1, 0)
                    elif event.key == pygame.K_LEFT:
                        direction = LEFT
                        new_grid = move_player(grid, 0, -1)
                    elif event.key == pygame.K_RIGHT:
                        direction = RIGHT
                        new_grid = move_player(grid, 0, 1)
                    elif event.key == pygame.K_z:
                        if history:
                            grid, direction, moves = history.pop()
                        continue
                    elif event.key == pygame.K_r:
                        grid, level_name, difficulty, direction, history, moves = load_level(current_level)
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        surface = display_game.resize_to_menu(surface)
                        state = STATE_SELECT
                        continue

                    if new_grid is not grid:
                        history.append(([row[:] for row in grid], direction, moves))
                        grid  = new_grid
                        moves += 1

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons["undo"].collidepoint(mouse_pos) and history:
                        grid, direction, moves = history.pop()
                    elif buttons["reset"].collidepoint(mouse_pos):
                        grid, level_name, difficulty, direction, history, moves = load_level(current_level)
                    elif buttons["quit"].collidepoint(mouse_pos):
                        surface = display_game.resize_to_menu(surface)
                        state = STATE_SELECT

        if state == STATE_MENU:
            display_game.draw_menu(surface, font_title, font, mouse_pos)

        elif state == STATE_SELECT:
            display_game.draw_level_select(
                surface, font_title, font, mouse_pos,
                LEVELS, select_page, select_diff
            )

        elif state == STATE_PLAYING:
            display_game.draw_grid(surface, grid, sprites, direction)
            display_game.draw_ui(surface, font, buttons, mouse_pos, moves)

            if is_won(grid):
                overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))
                surface.blit(overlay, (0, 0))

                win_text = font_title.render("Bravo !", True, (255, 220, 50))
                sub_text = font.render(f"{level_name} résolu en {moves} coups !", True, (255, 240, 200))
                hint     = font.render("Entrée = niveau suivant", True, (200, 200, 200))

                for surf, dy in [(win_text, -50), (sub_text, 20), (hint, 60)]:
                    sx = (surface.get_width() - surf.get_width()) // 2
                    sy = (surface.get_height() - surf.get_height()) // 2 + dy
                    surface.blit(surf, (sx, sy))

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    next_level = current_level + 1
                    if next_level < level_count():
                        current_level = next_level
                        grid, level_name, difficulty, direction, history, moves = load_level(current_level)
                        surface, buttons = display_game.resize_display(grid)
                    else:
                        state = STATE_MENU

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

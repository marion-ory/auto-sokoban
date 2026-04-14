import pygame
import importlib
display_game = importlib.import_module("display-game")
from constants import *

test_grid = [
    [-1, -1, -1, -1, -1, -1, -1],
    [-1,  0,  0,  1,  0,  0, -1],
    [-1,  0,  2,  0,  0,  0, -1],
    [-1,  0,  0,  3,  0,  0, -1],
    [-1,  0,  0,  0,  4,  0, -1],
    [-1,  0,  0,  0,  0,  0, -1],
    [-1, -1, -1, -1, -1, -1, -1],
]

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

def reset_game():
    return [row[:] for row in test_grid], DOWN, [], 0

def main():
    grid, direction, history, moves = reset_game()
    state = STATE_MENU

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
                    menu_buttons = display_game.draw_menu(surface, font_title, font, mouse_pos)
                    if menu_buttons["play"].collidepoint(mouse_pos):
                        grid, direction, history, moves = reset_game()
                        state = STATE_PLAYING
                    elif menu_buttons["quit"].collidepoint(mouse_pos):
                        running = False

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
                        grid, direction, history, moves = reset_game()
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        state = STATE_MENU
                        continue

                    if new_grid is not grid:
                        history.append(([row[:] for row in grid], direction, moves))
                        grid  = new_grid
                        moves += 1

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons["undo"].collidepoint(mouse_pos) and history:
                        grid, direction, moves = history.pop()
                    elif buttons["reset"].collidepoint(mouse_pos):
                        grid, direction, history, moves = reset_game()
                    elif buttons["quit"].collidepoint(mouse_pos):
                        state = STATE_MENU

        if state == STATE_MENU:
            display_game.draw_menu(surface, font_title, font, mouse_pos)

        elif state == STATE_PLAYING:
            display_game.draw_grid(surface, grid, sprites, direction)
            display_game.draw_ui(surface, font, buttons, mouse_pos, moves)

            if is_won(grid):
                win_text = font_title.render("Bravo !", True, (255, 220, 50))
                sub_text = font.render(f"Résolu en {moves} coups", True, (255, 240, 200))
                wx = (surface.get_width() - win_text.get_width()) // 2
                wy = (surface.get_height() - win_text.get_height()) // 2
                surface.blit(win_text, (wx, wy))
                surface.blit(sub_text, ((surface.get_width() - sub_text.get_width()) // 2, wy + win_text.get_height() + 5))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

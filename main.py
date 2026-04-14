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

def main():
    grid = [row[:] for row in test_grid]
    direction = DOWN

    surface, sprites = display_game.init_display(grid)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    direction = DOWN
                    grid = move_player(grid, 1, 0)
                elif event.key == pygame.K_UP:
                    direction = UP
                    grid = move_player(grid, -1, 0)
                elif event.key == pygame.K_LEFT:
                    direction = LEFT
                    grid = move_player(grid, 0, -1)
                elif event.key == pygame.K_RIGHT:
                    direction = RIGHT
                    grid = move_player(grid, 0, 1)

        display_game.draw_grid(surface, grid, sprites, direction)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

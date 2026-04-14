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

def main():
    surface, sprites = display_game.init_display(test_grid)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display_game.draw_grid(surface, test_grid, sprites)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

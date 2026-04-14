import pygame
import importlib
# Les fichiers avec tirets ne peuvent pas être importés directement
display_game = importlib.import_module("display-game")
build_game   = importlib.import_module("build-game")
from constants import *
from levels import get_level, level_count, LEVELS

# Mapping direction → (dr, dc) pour rejouer les coups du solver
MOVE_MAP = {
    UP:    (-1,  0),
    DOWN:  ( 1,  0),
    LEFT:  ( 0, -1),
    RIGHT: ( 0,  1),
}
SOLVE_DELAY = 300  # millisecondes entre chaque coup animé

def find_player(grid):
    # Parcourt la grille et retourne les coordonnées (ligne, colonne) du joueur
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == PLAYER or cell == PLAYER_ON_TARGET:
                return r, c
    return None

def move_player(grid, dr, dc):
    # dr/dc = direction : ex. (-1, 0) = haut, (0, 1) = droite
    pos = find_player(grid)
    if pos is None:
        return grid

    r, c = pos
    nr, nc = r + dr, c + dc  # case cible du joueur

    if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0])):
        return grid
    if grid[nr][nc] == WALL:
        return grid

    # On travaille sur une copie pour ne pas modifier l'état actuel
    new_grid = [row[:] for row in grid]
    target_cell = grid[nr][nc]

    # Si la case cible contient une caisse, on tente de la pousser
    if target_cell == BOX or target_cell == BOX_ON_TARGET:
        br, bc = nr + dr, nc + dc  # case derrière la caisse
        if not (0 <= br < len(grid) and 0 <= bc < len(grid[0])):
            return grid
        if grid[br][bc] == WALL or grid[br][bc] == BOX or grid[br][bc] == BOX_ON_TARGET:
            return grid  # caisse bloquée, mouvement impossible
        new_grid[br][bc] = BOX_ON_TARGET if grid[br][bc] == TARGET else BOX

    # Déplacer le joueur (en conservant la cible s'il était dessus)
    new_grid[nr][nc] = PLAYER_ON_TARGET if (target_cell == TARGET or target_cell == BOX_ON_TARGET) else PLAYER
    new_grid[r][c] = TARGET if grid[r][c] == PLAYER_ON_TARGET else EMPTY

    return new_grid

def is_won(grid):
    # Victoire = aucune caisse non posée (toutes les BOX ont disparu)
    for row in grid:
        if BOX in row:
            return False
    return True

def load_level(index):
    grid, name, difficulty = get_level(index)
    return grid, name, difficulty, DOWN, [], 0  # grille, nom, diff, direction, historique, coups

def cancel_solve(solving, solution):
    # Annule l'animation en cours du solver
    return False, []

def main():
    current_level = 0
    grid, level_name, difficulty, direction, history, moves = load_level(current_level)

    # États du jeu : MENU → SELECT → PLAYING
    state       = STATE_MENU
    select_page = 0
    select_diff = "Tous"

    # Variables du solver
    solving         = False
    solution        = []
    last_solve_time = 0
    solver_algo     = "A*"  # algorithme sélectionné : "DFS", "BFS" ou "A*"

    game_surface, display_surface, scale, sprites, font, font_title, buttons = display_game.init_display(grid)
    clock   = pygame.time.Clock()
    running = True

    while running:
        # Convertit la position souris en coordonnées de la surface interne (avant scaling)
        raw = pygame.mouse.get_pos()
        mouse_pos = (int(raw[0] / scale), int(raw[1] / scale))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu_btns = display_game.draw_menu(game_surface, font_title, font, mouse_pos)
                    if menu_btns["play"].collidepoint(mouse_pos):
                        game_surface, display_surface, scale = display_game.resize_to_menu()
                        state = STATE_SELECT
                    elif menu_btns["quit"].collidepoint(mouse_pos):
                        running = False

            elif state == STATE_SELECT:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    sel_btns = display_game.draw_level_select(
                        game_surface, font_title, font, mouse_pos,
                        LEVELS, select_page, select_diff
                    )

                    # Changer le filtre de difficulté et revenir à la page 0
                    for diff in DIFFICULTIES:
                        if f"filter_{diff}" in sel_btns and sel_btns[f"filter_{diff}"].collidepoint(mouse_pos):
                            select_diff = diff
                            select_page = 0

                    # Lancer un niveau sélectionné
                    for slot in range(LEVELS_PER_PAGE):
                        key = f"level_{slot}"
                        if key in sel_btns:
                            rect, real_idx = sel_btns[key]
                            if rect.collidepoint(mouse_pos):
                                current_level = real_idx
                                grid, level_name, difficulty, direction, history, moves = load_level(current_level)
                                game_surface, display_surface, scale, buttons = display_game.resize_display(grid)
                                state = STATE_PLAYING

                    if "prev" in sel_btns and sel_btns["prev"].collidepoint(mouse_pos):
                        select_page -= 1
                    if "next" in sel_btns and sel_btns["next"].collidepoint(mouse_pos):
                        select_page += 1
                    if "back" in sel_btns and sel_btns["back"].collidepoint(mouse_pos):
                        game_surface, display_surface, scale = display_game.resize_to_menu()
                        state = STATE_MENU

            elif state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    # Toute touche annule l'animation du solver
                    if solving:
                        solving, solution = cancel_solve(solving, solution)
                        continue

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
                        # Undo : restaure le dernier état sauvegardé
                        if history:
                            grid, direction, moves = history.pop()
                        continue
                    elif event.key == pygame.K_r:
                        grid, level_name, difficulty, direction, history, moves = load_level(current_level)
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        game_surface, display_surface, scale = display_game.resize_to_menu()
                        state = STATE_SELECT
                        continue

                    # Si le mouvement a changé la grille, on sauvegarde l'état précédent
                    if new_grid is not grid:
                        history.append(([row[:] for row in grid], direction, moves))
                        grid  = new_grid
                        moves += 1

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons["undo"].collidepoint(mouse_pos) and history:
                        solving, solution = cancel_solve(solving, solution)
                        grid, direction, moves = history.pop()
                    elif buttons["reset"].collidepoint(mouse_pos):
                        solving, solution = cancel_solve(solving, solution)
                        grid, level_name, difficulty, direction, history, moves = load_level(current_level)
                    elif buttons["quit"].collidepoint(mouse_pos):
                        solving, solution = cancel_solve(solving, solution)
                        game_surface, display_surface, scale = display_game.resize_to_menu()
                        state = STATE_SELECT
                    elif buttons["algo"].collidepoint(mouse_pos):
                        # Cycle entre les algorithmes disponibles
                        idx         = build_game.ALGOS.index(solver_algo)
                        solver_algo = build_game.ALGOS[(idx + 1) % len(build_game.ALGOS)]
                    elif buttons["solve"].collidepoint(mouse_pos):
                        if solving:
                            solving, solution = cancel_solve(solving, solution)
                        else:
                            result = build_game.solve(grid, solver_algo)
                            if result:
                                solution        = result
                                solving         = True
                                last_solve_time = pygame.time.get_ticks()

        # ── Rendu selon l'état courant ──
        if state == STATE_MENU:
            display_game.draw_menu(game_surface, font_title, font, mouse_pos)

        elif state == STATE_SELECT:
            display_game.draw_level_select(
                game_surface, font_title, font, mouse_pos,
                LEVELS, select_page, select_diff
            )

        elif state == STATE_PLAYING:
            # ── Animation du solver : applique un coup toutes les SOLVE_DELAY ms ──
            if solving:
                now = pygame.time.get_ticks()
                if now - last_solve_time >= SOLVE_DELAY:
                    if solution:
                        move_dir        = solution.pop(0)
                        dr, dc          = MOVE_MAP[move_dir]
                        new_grid        = move_player(grid, dr, dc)
                        if new_grid is not grid:
                            history.append(([row[:] for row in grid], direction, moves))
                            grid      = new_grid
                            direction = move_dir
                            moves    += 1
                        last_solve_time = now
                    else:
                        # Plus de coups à jouer : animation terminée
                        solving = False

            display_game.draw_grid(game_surface, grid, sprites, direction)
            display_game.draw_ui(game_surface, font, buttons, mouse_pos, moves, solving, solver_algo)

            if is_won(grid):
                # Superposer un voile sombre semi-transparent
                overlay = pygame.Surface((game_surface.get_width(), game_surface.get_height()), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 120))
                game_surface.blit(overlay, (0, 0))

                win_text = font_title.render("Bravo !", True, (255, 220, 50))
                sub_text = font.render(f"{level_name} résolu en {moves} coups !", True, (255, 240, 200))
                hint     = font.render("Entrée = niveau suivant", True, (200, 200, 200))

                for surf, dy in [(win_text, -50), (sub_text, 20), (hint, 60)]:
                    sx = (game_surface.get_width() - surf.get_width()) // 2
                    sy = (game_surface.get_height() - surf.get_height()) // 2 + dy
                    game_surface.blit(surf, (sx, sy))

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    next_level = current_level + 1
                    if next_level < level_count():
                        current_level = next_level
                        grid, level_name, difficulty, direction, history, moves = load_level(current_level)
                        game_surface, display_surface, scale, buttons = display_game.resize_display(grid)
                    else:
                        state = STATE_MENU

        # ── Affichage : scale la surface interne vers la fenêtre puis flip ──
        if scale < 1.0:
            pygame.transform.scale(game_surface, display_surface.get_size(), display_surface)
        else:
            display_surface.blit(game_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

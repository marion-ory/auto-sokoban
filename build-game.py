from constants import *

# ─── Fonctions de jeu (dupliquées ici pour éviter l'import circulaire avec main.py) ──

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

# ─── Solver DFS ───────────────────────────────────────────────────────────────
# Retourne la liste des directions à jouer pour résoudre le niveau,
# ou None si aucune solution n'est trouvée.
# Directions : constantes UP / DOWN / LEFT / RIGHT de constants.py

def grid_to_state(grid):
    # Convertit la grille en tuple de tuples (immuable) pour pouvoir
    # l'utiliser comme clé dans l'ensemble "visited"
    return tuple(tuple(row) for row in grid)

def solve(initial_grid):
    # DFS : explore chaque chemin jusqu'au bout avant d'en essayer un autre (pile)
    stack   = [(initial_grid, [])]
    visited = {grid_to_state(initial_grid)}

    directions = [
        (UP,    -1,  0),
        (DOWN,   1,  0),
        (LEFT,   0, -1),
        (RIGHT,  0,  1),
    ]

    while stack:
        current_grid, path = stack.pop()  # dernier état ajouté (LIFO)

        if is_won(current_grid):
            return path

        for name, dr, dc in directions:
            new_grid = move_player(current_grid, dr, dc)
            if new_grid is not current_grid:
                state = grid_to_state(new_grid)
                if state not in visited:
                    visited.add(state)
                    stack.append((new_grid, path + [name]))

    return None

from constants import *
from collections import deque
import heapq

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

# ─── Utilitaires communs ──────────────────────────────────────────────────────

def grid_to_state(grid):
    # Convertit la grille en tuple de tuples (immuable) pour l'utiliser comme clé
    return tuple(tuple(row) for row in grid)

DIRECTIONS = [
    (UP,    -1,  0),
    (DOWN,   1,  0),
    (LEFT,   0, -1),
    (RIGHT,  0,  1),
]

MAX_STATES = 300_000  # limite pour éviter de freezer sur les niveaux très complexes

# ─── DFS (Depth-First Search) ─────────────────────────────────────────────────
# Explore chaque chemin jusqu'au bout avant d'en essayer un autre.
# Rapide mais ne garantit pas la solution la plus courte.

def solve_dfs(initial_grid):
    stack   = [(initial_grid, [])]
    visited = {grid_to_state(initial_grid)}

    while stack:
        if len(visited) > MAX_STATES:
            return None
        current_grid, path = stack.pop()
        if is_won(current_grid):
            return path
        for name, dr, dc in DIRECTIONS:
            new_grid = move_player(current_grid, dr, dc)
            if new_grid is not current_grid:
                state = grid_to_state(new_grid)
                if state not in visited:
                    visited.add(state)
                    stack.append((new_grid, path + [name]))
    return None

# ─── BFS (Breadth-First Search) ───────────────────────────────────────────────
# Explore niveau par niveau : garantit la solution en nombre de coups minimal.
# Plus lent que A* sur les grands niveaux.

def solve_bfs(initial_grid):
    queue   = deque([(initial_grid, [])])
    visited = {grid_to_state(initial_grid)}

    while queue:
        if len(visited) > MAX_STATES:
            return None
        current_grid, path = queue.popleft()
        if is_won(current_grid):
            return path
        for name, dr, dc in DIRECTIONS:
            new_grid = move_player(current_grid, dr, dc)
            if new_grid is not current_grid:
                state = grid_to_state(new_grid)
                if state not in visited:
                    visited.add(state)
                    queue.append((new_grid, path + [name]))
    return None

# ─── A* ───────────────────────────────────────────────────────────────────────
# Guidé par une heuristique : explore en priorité les états les plus prometteurs.
# Garantit la solution optimale avec une heuristique admissible.
#
# Heuristique : somme des distances de Manhattan entre chaque caisse
# et la cible libre la plus proche → sous-estimation garantie (admissible).

def heuristic(grid):
    boxes   = [(r, c) for r, row in enumerate(grid)
               for c, cell in enumerate(row) if cell == BOX]
    targets = [(r, c) for r, row in enumerate(grid)
               for c, cell in enumerate(row) if cell in (TARGET, PLAYER_ON_TARGET)]
    if not boxes:
        return 0
    return sum(min(abs(br - tr) + abs(bc - tc) for tr, tc in targets)
               for br, bc in boxes) if targets else 0

def solve_astar(initial_grid):
    h0      = heuristic(initial_grid)
    counter = 0  # départage les égalités dans le tas sans comparer les grilles
    # tas : (f, g, counter, état, grille, chemin)
    heap    = [(h0, 0, counter, grid_to_state(initial_grid), initial_grid, [])]
    best_g  = {grid_to_state(initial_grid): 0}  # meilleur coût connu pour chaque état

    while heap:
        if len(best_g) > MAX_STATES:
            return None
        f, g, _, state, current_grid, path = heapq.heappop(heap)

        if is_won(current_grid):
            return path
        if g > best_g.get(state, float('inf')):
            continue  # un meilleur chemin vers cet état a déjà été trouvé

        for name, dr, dc in DIRECTIONS:
            new_grid = move_player(current_grid, dr, dc)
            if new_grid is not current_grid:
                new_state = grid_to_state(new_grid)
                new_g     = g + 1
                if new_g < best_g.get(new_state, float('inf')):
                    best_g[new_state] = new_g
                    counter += 1
                    heapq.heappush(heap, (new_g + heuristic(new_grid),
                                          new_g, counter,
                                          new_state, new_grid,
                                          path + [name]))
    return None

# ─── Dispatcher ───────────────────────────────────────────────────────────────

ALGOS = ["DFS", "BFS", "A*"]  # ordre de cycle dans l'interface

def solve(grid, algo="A*"):
    if algo == "DFS":
        return solve_dfs(grid)
    elif algo == "BFS":
        return solve_bfs(grid)
    else:
        return solve_astar(grid)

from constants import *
import main
from collections import deque
import heapq

def grid_to_state(grid):
    # Rend la grille hashable (tuple) pour l'utiliser comme clé dans un set/dict
    return tuple(tuple(row) for row in grid)

def solve_dfs(initial_grid):
    stack = [(initial_grid, [])]
    visited = {grid_to_state(initial_grid)}
    directions = [(UP, -1, 0), (DOWN, 1, 0), (LEFT, 0, -1), (RIGHT, 0, 1)]

    print("[DFS] Recherche en cours...")

    while stack:
        current_grid, path = stack.pop()

        if main.is_won(current_grid):
            print(f"[DFS] Solution trouvée : {len(path)} coups")
            return path

        for name, dr, dc in directions:
            new_grid = main.move_player(current_grid, dr, dc)
            
            if new_grid is not current_grid:
                state = grid_to_state(new_grid)
                if state not in visited:
                    visited.add(state)
                    stack.append((new_grid, path + [name]))

    print("[DFS] Aucune solution.")
    return None

def solve_bfs(initial_grid):
    queue = deque([(initial_grid, [])])
    visited = {grid_to_state(initial_grid)}
    directions = [(UP, -1, 0), (DOWN, 1, 0), (LEFT, 0, -1), (RIGHT, 0, 1)]

    print("[BFS] Recherche en cours...")

    while queue:
        # Différence avec DFS : on popleft() pour explorer en largeur
        current_grid, path = queue.popleft()

        if main.is_won(current_grid):
            print(f"[BFS] Solution trouvée : {len(path)} coups")
            return path

        for name, dr, dc in directions:
            new_grid = main.move_player(current_grid, dr, dc)
            
            if new_grid is not current_grid:
                state = grid_to_state(new_grid)
                if state not in visited:
                    visited.add(state)
                    queue.append((new_grid, path + [name]))

    print("[BFS] Aucune solution.")
    return None

def get_targets(grid):
    targets = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell in (TARGET, BOX_ON_TARGET, PLAYER_ON_TARGET):
                targets.append((r, c))
    return targets

def get_boxes(grid):
    boxes = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell in (BOX, BOX_ON_TARGET):
                boxes.append((r, c))
    return boxes

def heuristique(grid, targets):
    # Distance de Manhattan : distance entre chaque caisse et la cible la plus proche
    boxes = get_boxes(grid)
    total = 0
    for br, bc in boxes:
        total += min(abs(br - tr) + abs(bc - tc) for tr, tc in targets)
    return total

def solve_astar(initial_grid):
    targets = get_targets(initial_grid)
    start_state = grid_to_state(initial_grid)
    
    counter = 0 # Compteur pour éviter le crash de heapq sur la comparaison de grilles
    g_score = 0
    h_score = heuristique(initial_grid, targets)
    
    # Priority queue : (f_score, g_score, id_unique, grille, chemin)
    queue = [(g_score + h_score, g_score, counter, initial_grid, [])]
    
    # Stocke le meilleur g_score trouvé pour un état donné
    visited = {start_state: g_score}
    directions = [(UP, -1, 0), (DOWN, 1, 0), (LEFT, 0, -1), (RIGHT, 0, 1)]

    print("[A*] Recherche en cours...")

    while queue:
        f, g, _, current_grid, path = heapq.heappop(queue)

        if main.is_won(current_grid):
            print(f"[A*] Solution trouvée : {len(path)} coups")
            return path

        for name, dr, dc in directions:
            new_grid = main.move_player(current_grid, dr, dc)
            
            if new_grid is not current_grid:
                state = grid_to_state(new_grid)
                nouveau_g = g + 1
                
                # Mise à jour si nouvel état ou chemin plus court
                if state not in visited or nouveau_g < visited[state]:
                    visited[state] = nouveau_g
                    h = heuristique(new_grid, targets)
                    
                    counter += 1
                    heapq.heappush(queue, (nouveau_g + h, nouveau_g, counter, new_grid, path + [name]))

    print("[A*] Aucune solution.")
    return None
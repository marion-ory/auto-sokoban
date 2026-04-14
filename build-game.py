from constants import *
import main

def grid_to_state(grid):
    # On transforme la liste en tuples pour pouvoir l'utiliser comme clé 
    # (le set 'visited' n'accepte que des objets immuables)
    return tuple(tuple(row) for row in grid)

def solve(initial_grid):
    #on essaie chaque chemin possible jusqu'à trouver la sortie
    stack = [(initial_grid, [])]
    
    # On garde une trace de ce qu'on a déjà testé pour pas boucler à l'infini
    visited = {grid_to_state(initial_grid)}
    
    # Vecteurs de déplacement
    directions = [
        (UP,    -1,  0),
        (DOWN,   1,  0),
        (LEFT,   0, -1),
        (RIGHT,  0,  1)
    ]

    print("DFS : C'est parti, je cherche...")

    while stack:
        # On récupère le dernier état ajouté (principe de la pile)
        current_grid, path = stack.pop()

        # Si toutes les caisses sont placées, c'est gagné
        if main.is_won(current_grid):
            print(f"Trouvé ! ({len(path)} coups)")
            return path

        for name, dr, dc in directions:
            # On simule le mouvement
            new_grid = main.move_player(current_grid, dr, dc)
            
            # Si le perso a pu bouger, on analyse le résultat
            if new_grid is not current_grid:
                state = grid_to_state(new_grid)
                
                # Si cette configuration de plateau est inédite, on l'ajoute à la pile
                if state not in visited:
                    visited.add(state)
                    stack.append((new_grid, path + [name]))

    print("DFS : Impasse totale, aucune solution.")
    return None
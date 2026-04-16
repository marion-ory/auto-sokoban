import heapq  # Trie les priorités
from solver import EtatJeu, direction
import map
from loop import reconstruire_chemin


# ========= Distance Manathan ========== #


def heuristique(box_pos, targets):
    total = 0

    # distance entre caisse et cible la + proche
    for b in box_pos:
        distance = min(abs(b[0] - t[0]) + abs(b[1] - t[1]) for t in targets)
        toltal += distance
    return total


def solve_astar(etat_initial, wall, targets):
    targets_tuple = tuple(sorted(targets))
    # on stock point de depart box_pos & pos de la cible
    start_f = heuristique(etat_initial.box_pos, targets_tuple)
    queue = [(start_f, 0, etat_initial)]

    visites = {etat_initial: 0}
    parents = {}

    while queue:
        # 1. on sort le plus petit score
        f, g, etat_actuel = heapq.heappop(queue)

        # Verifie victoire
        if etat_actuel.box_pos == targets_tuple:
            return reconstruire_chemin(etat_actuel, parents)

        # 3.Check les cases voisines
        for dir_nom in direction:
            voisin = etat_actuel.move(dir_nom, wall)

            if voisin is not None:
                nouveau_g = g + 1  # on a fait un pas de plus

                # si c'est un nouvel ou que j ai un chemin plus court pour y arriver

                if voisin not in visites or nouveau_g < visites[voisin]:
                    visites[voisin] = nouveau_g
                    h = heuristique(voisin.box_pos, targets_tuple)
                    f_score = nouveau_g + h  # f = g+h

                    parents[voisin] = (etat_actuel, dir_nom)
                    heapq.heappush(queue, (f_score, nouveau_g, voisin))
        return None

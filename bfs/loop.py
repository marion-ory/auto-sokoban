from collections import deque
from solver import EtatJeu, direction
import map


def solve_sokoban(etat_initial, wall, targets):
    queue = deque([etat_initial])
    visites = {etat_initial}
    parents = {}
    # stocke (chq etat et chq direction etape par etape jusqu à la victoire)

    targets_tuple = tuple(sorted(targets))
    # on Tri pour eviter les doublons de position dans les cibles

    while queue:
        # 1 - Recupere l etat le plus ancien
        etat_actuel = queue.popleft()

        # 2- Verifie victoire
        if etat_actuel.box_pos == targets_tuple:
            return reconstruire_chemin(etat_actuel, parents)

        # 3- Check les cases voisines
        for dir_nom in direction:
            voisin = etat_actuel.move(dir_nom, wall)

            # 4- Si le mouvement est possible que joueur n est jamais passé par
            if voisin is not None and voisin not in visites:
                visites.add(voisin)  # on ajoute le deplacement aux visites
                parents[voisin] = (etat_actuel, dir_nom)
                queue.append(voisin)

    return None


# Pas de solution


def reconstruire_chemin(etat_final, parents):
    chemin = []
    etat_actuel = etat_final

    # Tant que l'etat etat_actuel a un parent dans notre dictionnaire
    while etat_actuel in parents:
        parent, move_nom = parents[etat_actuel]
        chemin.append(move_nom)
        etat_actuel = parent

    return chemin[
        ::-1
    ]  # On inverse la liste car on est remonté de la fin vers le début


def extraire_donnees(matrice):
    player_pos = []
    box = []
    wall = set()  # fonction pour stock plusieurs items dans une variable
    targets = []

    for y, ligne in enumerate(matrice):
        for x, valeur in enumerate(ligne):
            if valeur == 3:
                player_pos = (x, y)
            elif valeur == 2:
                box.append((x, y))  # ajoute la nouvel pos
            elif valeur == -1:
                wall.add((x, y))  # on ajoute les coordonnes au wall
            elif valeur == 1:
                targets.append((x, y))  # on ajoute les coordonnees a target

    return player_pos, box, wall, targets


# 1. Extraction
# Assure-toi que map.NIVEAU_1 est bien défini dans ton fichier map.py
p, b, w, t = extraire_donnees(map.NIVEAU_1)

# 2. Création de l'état de départ
depart = EtatJeu(p, b)

# 3. Résolution
print("Calcul de la solution en cours...")
sol = solve_sokoban(depart, w, t)

print("Mouvements à faire :", sol)

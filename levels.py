from constants import *
import os

# ─── Conversion XSB → matrice ────────────────────────────────────────────────

def xsb_to_matrix(xsb):
    # Traduit un niveau au format XSB (texte) en matrice 2D d'entiers
    # Chaque caractère XSB correspond à une constante définie dans constants.py
    char_map = {
        '#': WALL,
        ' ': EMPTY,
        '.': TARGET,
        '$': BOX,
        '@': PLAYER,
        '*': BOX_ON_TARGET,
        '+': PLAYER_ON_TARGET,
    }
    lines = xsb.strip('\n').split('\n')
    max_width = max(len(line) for line in lines)
    matrix = []
    for line in lines:
        row = [char_map.get(c, WALL) for c in line]
        # Complète les lignes courtes avec des murs pour obtenir un rectangle
        while len(row) < max_width:
            row.append(WALL)
        matrix.append(row)
    return matrix

def count_boxes(xsb):
    # Compte le nombre total de caisses dans le niveau (posées ou non sur une cible)
    return xsb.count('$') + xsb.count('*')

def get_difficulty(boxes):
    # Classe la difficulté selon le nombre de caisses à placer
    if boxes <= 2:
        return "Facile"
    elif boxes <= 4:
        return "Moyen"
    else:
        return "Difficile"

# ─── Chargement du fichier Microban ──────────────────────────────────────────

def load_microban(filepath):
    # Parse le fichier microban.txt : les niveaux sont séparés par des lignes "; N"
    # Chaque niveau est converti en matrice et enrichi d'un nom et d'une difficulté
    levels = []
    with open(filepath, 'r') as f:
        content = f.read()

    current_lines = []
    number = 0

    for line in content.split('\n'):
        stripped = line.rstrip()

        if stripped.startswith(';'):
            # Fin du niveau précédent : on le sauvegarde avant de passer au suivant
            if current_lines:
                xsb = '\n'.join(current_lines)
                boxes = count_boxes(xsb)
                levels.append({
                    "name": f"Niveau {number}",
                    "difficulty": get_difficulty(boxes),
                    "grid": xsb_to_matrix(xsb),
                })
                current_lines = []
            # Extraire le numéro du niveau si la ligne est de la forme "; N"
            parts = stripped[1:].strip()
            if parts.isdigit():
                number = int(parts)
        elif stripped == '':
            continue
        else:
            current_lines.append(line.rstrip())

    # Sauvegarde du dernier niveau (pas suivi d'une ligne ";")
    if current_lines:
        xsb = '\n'.join(current_lines)
        boxes = count_boxes(xsb)
        levels.append({
            "name": f"Niveau {number}",
            "difficulty": get_difficulty(boxes),
            "grid": xsb_to_matrix(xsb),
        })

    return levels

# ─── Chargement au démarrage ──────────────────────────────────────────────────

# Résout le chemin vers microban.txt de façon portable (relatif à ce fichier)
_microban_path = os.path.join(os.path.dirname(__file__), 'microban.txt')
LEVELS = load_microban(_microban_path)  # liste de dict {name, difficulty, grid} chargée une seule fois

def get_level(index):
    # Retourne une copie profonde de la grille pour ne pas altérer l'original
    level = LEVELS[index]
    return [row[:] for row in level["grid"]], level["name"], level["difficulty"]

def level_count():
    return len(LEVELS)

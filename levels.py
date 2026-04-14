from constants import *
import os

# ─── Conversion XSB → matrice ────────────────────────────────────────────────

def xsb_to_matrix(xsb):
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
        while len(row) < max_width:
            row.append(WALL)
        matrix.append(row)
    return matrix

def count_boxes(xsb):
    return xsb.count('$') + xsb.count('*')

def get_difficulty(boxes):
    if boxes <= 2:
        return "Facile"
    elif boxes <= 4:
        return "Moyen"
    else:
        return "Difficile"

# ─── Chargement du fichier Microban ──────────────────────────────────────────

def load_microban(filepath):
    levels = []
    with open(filepath, 'r') as f:
        content = f.read()

    current_lines = []
    number = 0

    for line in content.split('\n'):
        stripped = line.rstrip()

        if stripped.startswith(';'):
            # Si on avait un niveau en cours, on le sauvegarde
            if current_lines:
                xsb = '\n'.join(current_lines)
                boxes = count_boxes(xsb)
                levels.append({
                    "name": f"Niveau {number}",
                    "difficulty": get_difficulty(boxes),
                    "grid": xsb_to_matrix(xsb),
                })
                current_lines = []
            # Extraire le numéro du niveau si c'est "; N"
            parts = stripped[1:].strip()
            if parts.isdigit():
                number = int(parts)
        elif stripped == '':
            continue
        else:
            current_lines.append(line.rstrip())

    # Dernier niveau
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

_microban_path = os.path.join(os.path.dirname(__file__), 'microban.txt')
LEVELS = load_microban(_microban_path)

def get_level(index):
    level = LEVELS[index]
    return [row[:] for row in level["grid"]], level["name"], level["difficulty"]

def level_count():
    return len(LEVELS)

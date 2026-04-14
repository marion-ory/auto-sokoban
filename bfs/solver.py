import map

# ====================[Recupere & stock la map et position initiale]====================#
map = []
box = []
player = []

direction = {"Droite": (1, 0), "Gauche": (-1, 0), "Haut": (0, -1), "Bas": (0, 1)}
# haut= -1 pour pygame


class EtatJeu:
    def __init__(self, player_pos, box_pos):
        self.player_pos = player_pos
        self.box_pos = tuple(sorted(box_pos))

    # Gestion egalité des position :

    def __eq__(self, other):
        return self.player_pos == other.player_pos and self.box_pos == other.box_pos

    # Renvoi un int pour savoir si c est un nouvel état ou non

    def __hash__(self):
        return hash((self.player_pos, self.box_pos))

    # ---> Gestion des mouvements :
    # - Enregistre nouvelle position apres deplacement -#
    def move(self, dir_nom, wall):
        dx, dy = direction[dir_nom]
        nx, ny = self.player_pos[0] + dx, self.player_pos[1] + dy
        new_pos_player = (nx, ny)

        # - Player face mur -#
        if new_pos_player in wall:
            return None

        # - Player face caisse -#
        if new_pos_player in self.box_pos:
            # 1- verifie si la case derrière est vide
            box_nx, box_ny = nx + dx, ny + dy
            box_behind = (box_nx, box_ny)

            # 2- pas de murs pas d'autres casises
            if box_behind in wall or box_behind in self.box_pos:
                return None

            # 3- on enregistre la nouvelle position dans la liste
            new_box = list(self.box_pos)
            # 4- la caisse quitte cette case
            new_box.remove(new_pos_player)
            # 5- nouvelle pos de la box
            new_box.append(box_behind)

            # - On Retourne les nouvelles position
            return EtatJeu(new_pos_player, new_box)

        # Mouvement simple pas d'obstacle
        return EtatJeu(new_pos_player, self.box_pos)

    # Win la case est sur la cible :

    def is_win(self, targets):
        return self.box_pos == targets

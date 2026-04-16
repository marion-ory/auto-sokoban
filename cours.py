import heapq

# Create : BFS DFS ASTAR version optimus Prime

# la grille ou le labyrinthe 0= espace 1= Murs

grille = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
]
depart = (0, 0)
arrive = (4, 4)


def distance_manhattan(a, b):
    # La distance de manhattan est utilisée dans les grilles.
    # on ne peut pas transpercer les murs en diagonal donc on calcule:
    # distance=: [x-1-x-2] +[y1-y2]
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solveur_peda(mode="BFS"):
    rows, cols = len(grille), len(grille[0])

    # Astar : utilisé une fille de priorité : il trie les cases par score
    if mode == "A*":
        file_ou_pile = [(0, depart)]  # 2 arguments car on compare
    else:
        # bfs/dfs utilisent une liste simple
        # c'est l ordre de sortie (pop) qui fera la dif
        file_ou_pile = [depart]

    visites = {depart}
    etapes = 0
    print(f"Lancement du mode : {mode}")

    if mode == "BFS":
        print("j'explore comme une tache d'huile niveau par niveau ")
    elif mode == "DFS":
        print("j'explore comme l'OM")
    elif mode == "A*":
        print("comme une boussole(distance de mahanattan)")

    while file_ou_pile:
        etapes += 1

        # phase 3: la logique de selection le <3 de l'algo
        if mode == "BFS":
            # FIFO (first in fist out: premier arrivé premier servi)
            actuel = file_ou_pile.pop(0)

        elif mode == "DFS":
            # LIFO (last in last out: le dernier arrivé est le premier servi)
            actuel = file_ou_pile.pop()

        elif mode == "A*":
            # Priorité : on prends la case qui a le plus petit score (distance estimée)
            priorite, actuel = heapq.heappop(file_ou_pile)

        print(f"Etape {etapes} : je visite le case {actuel}")
        if actuel == arrive:
            print(f"succes ! arrivé trouve en {etapes} etapes.")
            return
        # phase 3: l'Exploration
        r, c = actuel
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc

        # condition de validite: condition de validation: dans la grille, pas un mur
        # et pas deja visité

        if (
            0 <= nr < rows
            and 0 <= nc < cols
            and grille[nr][nc] == 0
            and (nr, nc) not in visites
        ):
            visites.add((nr, nc))
            voisin = (nr, nc)

            if mode == "A*":
                # score =cout actuel (1) + estimation du futur (manhattan)
                h = distance_manhattan(voisin, arrive)
                f_score = 1 + h
                heapq.heappush(file_ou_pile, (f_score, voisin))
                print(f" ---> boussole: {voisin} semble être à {h} pas à la sortie")
            else:
                file_ou_pile.append(voisin)
                print(f"--> nouveau chemin : {voisin}")

        # Lancement de la comparaison
        # on commence par les methodes "aveugles, puis on finit par l'intelligente (A*)"


solveur_peda(mode="BFS")
solveur_peda(mode="DFS")
solveur_peda(mode="A*")

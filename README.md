# Auto Sokoban

Jeu de Sokoban avec résolution automatique, développé en Python avec Pygame.

## Contexte

Projet scolaire réalisé à La Plateforme. Le but est de développer un jeu de Sokoban jouable, puis d'y intégrer un algorithme de résolution automatique (BFS/DFS).

## Fonctionnalités

- Jeu Sokoban complet jouable au clavier (flèches directionnelles)
- Interface graphique en pixel art style farm (Pygame)
- 155 niveaux issus du set **Microban** de David W. Skinner (garantis solvables)
- Sélection de niveau avec filtre par difficulté (Facile / Moyen / Difficile) et pagination
- Annulation du dernier mouvement (`Z` ou bouton)
- Réinitialisation de la partie (`R` ou bouton)
- Compteur de coups
- Écran titre, menu principal, écran de victoire
- Résolution automatique via BFS/DFS *(à venir)*

## Lancer le jeu

```bash
pip install pygame
python3 main.py
```

## Structure du projet

| Fichier | Rôle |
|---|---|
| `main.py` | Point d'entrée — boucle de jeu, gestion des états et des inputs |
| `build-game.py` | Logique du jeu — mécaniques, algorithme de résolution |
| `display-game.py` | Interface graphique — rendu Pygame, menus, boutons |
| `constants.py` | Constantes partagées (valeurs de la grille, couleurs, tailles) |
| `levels.py` | Chargement et conversion des niveaux depuis `microban.txt` |
| `microban.txt` | 155 niveaux Microban au format XSB |
| `assets/` | Sprites pixel art (tileset farm, personnage, caisses) |

## Représentation de la grille

La carte est une matrice 2D d'entiers :

| Valeur | Constante | Élément |
|---|---|---|
| -1 | `WALL` | Mur |
| 0 | `EMPTY` | Case vide |
| 1 | `TARGET` | Emplacement cible |
| 2 | `BOX` | Caisse |
| 3 | `PLAYER` | Joueur |
| 4 | `BOX_ON_TARGET` | Caisse sur cible |
| 5 | `PLAYER_ON_TARGET` | Joueur sur cible |

## Contrôles

| Touche | Action |
|---|---|
| Flèches | Déplacer le joueur |
| `Z` | Annuler le dernier mouvement |
| `R` | Réinitialiser le niveau |
| `Échap` | Retour à la sélection |
| `Entrée` | Niveau suivant (après victoire) |

## Solution

### Partie 1 — Jeu jouable
La grille est représentée par une matrice. À chaque déplacement, on vérifie si la case cible est libre ou contient une caisse poussable. L'historique des états permet l'annulation.

### Partie 2 — Résolution automatique *(en cours)*
L'algorithme BFS (Breadth-First Search) explore tous les états possibles du jeu niveau par niveau, garantissant la solution en nombre de coups minimal.

## Crédits

- Niveaux : **Microban** par David W. Skinner
- Sprites : **Cozy Farm Tileset** (ellen0ra, itch.io), **Free Pack** (itch.io), **Crates** (itch.io)

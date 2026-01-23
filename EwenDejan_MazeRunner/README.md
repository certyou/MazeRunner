Voici un `README.md` minimaliste et efficace, basé sur le fichier `test_final.py` qui semble être votre point d'entrée principal.

---

# MazeRunner AI

Un programme de résolution de labyrinthes utilisant un **algorithme génétique** (évolution, mutation, sélection).

## Installation

Assurez-vous d'avoir Python installé, puis installez les dépendances :

```bash
pip install numpy matplotlib

```

## Lancement

Exécutez le script principal :

```bash
python test_final.py

```

## Résultats

Le programme va générer un labyrinthe, entraîner l'IA, et sauvegarder deux images à la fin de l'exécution :

* `mazes_visualization.png` : Comparaison entre le chemin optimal (Dijkstra) et le chemin trouvé par l'IA.
* `statistics.png` : Graphiques de l'évolution de la fitness et de la longueur des trajets.
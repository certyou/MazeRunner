from Maze import Maze
from GeneticAlgo import GeneticAlgo
import time
import matplotlib.pyplot as plt
import numpy as np

def display_and_save_mazes(maze, best_runner=None, original_dijkstra_map=None):
    """
    Affiche et sauvegarde les différentes visualisations du labyrinthe.
    """
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    fig.suptitle('Labyrinthes')
    d_map = original_dijkstra_map

    # labyrinthe de base
    ax = axs[0, 0]
    ax.imshow(maze.empty_maze)
    ax.set_title('labyrinthe de base')
    ax.set_xticks([])
    ax.set_yticks([])

    # solution optimale
    ax = axs[0, 1]
    maze_sol = maze.empty_maze.copy()
    m_temp = Maze(maze.size)
    m_temp.maze = maze_sol
    m_temp.start = maze.start
    m_temp.goal = maze.goal
    m_temp.map = np.copy(d_map)
    m_temp.solve(m_temp.start[0], m_temp.start[1])
    ax.imshow(m_temp.maze)
    ax.set_title('solution opti')
    ax.set_xticks([])
    ax.set_yticks([])

    # runner génétique
    ax = axs[1, 0]
    runner_on_maze = maze.maze.copy()
    cell = list(best_runner.get_start())
    path = best_runner.get_path()
    for direction in path:
        if direction >= 0: # mouvement valide
            move = maze.cardinal[direction]
            next_x, next_y = cell[0] + move[0], cell[1] + move[1]
            if 0 <= next_x < maze.size and 0 <= next_y < maze.size: # dans le labyrinthe
                runner_on_maze[cell[0]][cell[1]] = [0, 255, 0] # marque le chemin du runner en vert
                cell[0], cell[1] = next_x, next_y        
    runner_on_maze[cell[0]][cell[1]] = [0, 255, 0] # marque la dernière position du runner
    runner_on_maze[maze.goal[0]][maze.goal[1]] = [255, 0, 0] # but en rouge
    runner_on_maze[maze.start[0]][maze.start[1]] = [0, 0, 255] # départ en bleu
    ax.imshow(runner_on_maze)
    ax.set_title('genetic')
    ax.set_xticks([])
    ax.set_yticks([])

    # carte des distances de dijkstra
    ax = axs[1, 1]
    d_map_masked = np.ma.masked_where(d_map == -1, d_map)
    cmap = plt.cm.viridis
    cmap.set_bad(color='black')
    cax = ax.matshow(d_map_masked, cmap=cmap)
    fig.colorbar(cax, ax=ax)
    ax.set_title('distances de dijkstra')
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('mazes_visualization.png')
    plt.close(fig)

def display_and_save_stats(ga):
    """
    Affiche et sauvegarde les statistiques de l'algorithme génétique.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
    fig.suptitle('Statistiques de l\'Évolution Génétique', fontsize=16)

    # Graphique de la fitness
    ax1.plot(ga.best_fitness_history, label='Meilleure Fitness')
    ax1.plot(ga.fitness_avg_history, label='Fitness Moyenne')
    ax1.set_xlabel('Générations')
    ax1.set_ylabel('Fitness')
    ax1.set_title('Évolution de la Fitness')
    ax1.legend()
    ax1.grid(True)

    # Graphique de la longueur du chemin
    ax2.plot(ga.length_history, label='Longueur Moyenne du Chemin', color='orange')
    ax2.set_xlabel('Générations')
    ax2.set_ylabel('Longueur')
    ax2.set_title('Longueur Moyenne du Chemin des Runners')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('statistics.png')
    plt.close(fig)

def main():
    # Configuration
    MAZE_SIZE = 100 
    RUNNER_LENGTH = MAZE_SIZE * MAZE_SIZE
    POP_SIZE = 200
    MAX_GEN = 5000
    MUTATION_RATE = 0.1
    SELECTION_RATE = 0.5

    maze = Maze(MAZE_SIZE)
    maze.generate()
    maze.solve_from_random_coordonnates()
    original_dijkstra_map = np.copy(maze.map)
    print("\n--- lancement des générations ---")
    ga = GeneticAlgo(maze, RUNNER_LENGTH, POP_SIZE, MAX_GEN, MUTATION_RATE, SELECTION_RATE)
    start_time = time.time()
    best_runner = ga.evolution(resume_interval=100)
    duration = time.time() - start_time
    print(f"\nTemps d'exécution : {duration:.2f} secondes")
    print(f"goal reached: {best_runner.is_goal_reached()}")
    display_and_save_mazes(maze, best_runner, original_dijkstra_map)
    display_and_save_stats(ga)

if __name__ == "__main__":
    main()
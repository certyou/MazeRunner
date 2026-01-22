from Maze import Maze
from GeneticAlgo import GeneticAlgo
import time

def main():
    # 1. Configuration
    MAZE_SIZE = 20          # Taille raisonnable pour tester rapidement
    RUNNER_LENGTH = MAZE_SIZE * MAZE_SIZE * 2  # Assez de mouvements pour atteindre le but
    POP_SIZE = 200
    MAX_GEN = 1000
    MUTATION_RATE = 0.1    # 5% de chance de mutation
    SELECTION_RATE = 0.2    # On garde les 30% meilleurs parents

    print("--- Génération du Labyrinthe ---")
    maze = Maze(MAZE_SIZE)
    maze.generate()
    # On définit départ et arrivée
    maze.solve_from_random_coordonnates() 
    print(f"Départ: {maze.get_start()} -> Objectif: {maze.get_goal()}")
    
    # Affichage du labyrinthe vierge (optionnel)
    # maze.display_map()

    print("\n--- Lancement de l'Algorithme Génétique ---")
    ga = GeneticAlgo(maze, RUNNER_LENGTH, POP_SIZE, MAX_GEN, MUTATION_RATE, SELECTION_RATE)
    
    start_time = time.time()
    best_runner = ga.evolution(resume_interval=10)

    duration = time.time() - start_time
    print(f"\nTemps d'exécution : {duration:.2f} secondes")
    print(f"Meilleure fitness finale : {best_runner.get_fitness()}")

    # 2. Visualisation des résultats
    print("Affichage de la solution et de la courbe de convergence...")
    
    # Afficher le chemin du meilleur runner sur le labyrinthe
    maze.display_runner(best_runner)
    
    # Afficher la courbe d'évolution
    ga.plot_stats()

if __name__ == "__main__":
    main()
from OldMaze import Maze
from Maze import Maze
from GeneticAlgo import GeneticAlgo
import time
import matplotlib.pyplot as plt


# ====== complexity ======
# in the worst case, we have:
#   - generate: O(n), with n, the number of cells (in this case x**2)
#   - check_neighbours: O(1)
#   - check_elegibility: O(1)
# ---> in total: we get O(16n)

"""test2 = Maze(50)
test2.generate()
test2.solve_from_random_coordonnates()
test2.display_soluce()"""

"""abscisse = [8, 16, 32, 64, 128, 256, 512]
ordonnee = []
for k in abscisse:
    start = time.time()
    test = UglyMaze(k)
    test.generate()
    test.dijkstra()
    test.solve(k-1,k-1)
    stop = time.time()-start
    ordonnee.append(stop)
plt.plot(abscisse, ordonnee, 'ro')
plt.show()"""

gen = GeneticAlgo(10, 10, 10)
gen.selection(0.8)
print(gen)
gen.display_best_runner()
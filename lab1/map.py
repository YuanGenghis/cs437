import numpy as np
import matplotlib.pyplot as plt

from pathsolver import PathSolver

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = np.zeros((self.height, self.width), dtype=np.uint8)
    
    def set_obstacle(self, x, y, width, height):
        self.map[y:y+height, x:x+width] = 1
    
    def get_map(self):
        return self.map
    
    def get_map_viz(self):
        ret = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        ret[self.map == 1] = (255, 0, 0) # RED for obstacle
        ret[self.map == 2] = (0, 255, 0) # GREEN for car
        return ret
    
    def get_map_viz_with_path(self, path):
        viz = self.get_map_viz()
        for i in range(len(path) - 1):
            x, y = path[i]
            viz[y, x] = (0, 0, 255) # BLUE for path
        return viz

    def get_path(self, start, goal):
        solver = PathSolver(self.map)
        return solver.solve_for_path(start, goal)

if __name__ == '__main__':
    my_map = Map(200, 200)
    my_map.set_obstacle(60, 60, 80, 80)
    path = my_map.get_path((0, 0), (199, 199))
    print(path)
    viz = my_map.get_map_viz_with_path(path)
    plt.imshow(viz)
    plt.show()

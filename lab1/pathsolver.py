from astar import AStar
import numpy as np

class PathSolver(AStar):
    """AStar solver for binary map generated from ultrasonic reading and speed reading"""
    def __init__(self, binary_map):
        self.binary_map = binary_map
        self.width = self.binary_map.shape[1]
        self.height = self.binary_map.shape[0]
    
    def solve_for_path(self, start, goal):
        """returns a list of coordinates that form the shortest path from start to goal
           start and goal are (x,y) tuples"""
        path = self.astar(start, goal)
        return path

    def heuristic_cost_estimate(self, n1, n2):
        """computes the 'direct' distance between two (x,y) tuples"""
        (x1, y1) = n1
        (x2, y2) = n2
        
        # Use Manhattan distance
        return np.abs(x2 - x1) + np.abs(y2 - y1)

    def distance_between(self, n1, n2):
        """this method always returns 1, as two 'neighbors' are always adajcent
           and this method assumes that n1 and n2 are neighbors"""
        return 1

    def neighbors(self, node):
        """ for a given coordinate in the maze, returns up to 4 adjacent(north,east,south,west)
            nodes that can be reached (=any adjacent coordinate that is not a wall)
        """
        x, y = node

        ret_list = []
        for (nx, ny) in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.binary_map[ny, nx] == 0:
                    ret_list.append((nx, ny))

        return ret_list

if __name__ == '__main__':
	# generate an empty map
    my_map = np.zeros((10, 10), dtype=np.uint8)

    # add a wall
    my_map[3:7, 3:7] = 1

    solver = PathSolver(my_map)

    # return an iterator of coordinates [(nx, ny), ...]
    path = solver.solve_for_path((0, 0), (9, 9))

    print([i for i in path])

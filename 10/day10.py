import sys
import os
from shapely.geometry import Point, Polygon
import numpy as np

os.environ["TQDM_COLOUR"] = "#33ffaa"
from tqdm import tqdm, trange

DAY = 10


def read_input(part, use_example_input=False):
    global DAY
    if DAY < 10:
        DAY = "0" + str(DAY)
    example_filename = "example_input.txt" if part == 1 else "example_input2.txt"
    filename = example_filename if use_example_input else f'input{DAY}.txt'
    file = open(filename, mode='r')
    lines = file.read().splitlines()
    file.close()
    return lines


def preprocess_input(input):
    y_max = len(input)
    x_max = len(input[0])
    pipe_map = np.ndarray((y_max, x_max), dtype=object)
    start_pos = (0, 0)
    start_node = None
    for y in range(y_max):
        line = input[y]
        for x in range(x_max):
            symbol = line[x]
            node = Node(x, y, symbol)
            pipe_map[y, x] = node
            if symbol == 'S':
                start_pos = (y, x)
                start_node = node

    # add connections for the start node ('S')
    for node in pipe_map.flat:
        y = node.y
        x = node.x
        for c in node.connections:
            c_x = x + c[1]
            c_y = y + c[0]
            is_out_of_bounds = c_x >= pipe_map.shape[1] or c_y >= pipe_map.shape[0]
            if not is_out_of_bounds and pipe_map[c_y, c_x].symbol == start_node.symbol:
                inv_x = -1 * c[1]
                inv_y = -1 * c[0]
                start_node.connections.append((inv_y, inv_x))

    return pipe_map, start_pos


'''
 Symbols described with index connections y,x
    Symbol  Connection 1    Connection 2
    |       y+1, x          y-1, x
    -       y, x+1          y, x-1
    L       y-1, x          y, x+1
    J       y-1, x          y, x-1
    7       y+1, x          y, x-1
    F       y+1, x          y, x+1
    .       ------          ------
    S       any             any
'''


class Node:
    symbol_connections_map = {'|': [(1, 0), (-1, 0)],
                              '-': [(0, 1), (0, -1)],
                              'L': [(-1, 0), (0, 1)],
                              'J': [(-1, 0), (0, -1)],
                              '7': [(1, 0), (0, -1)],
                              'F': [(1, 0), (0, 1)],
                              '.': [],
                              'S': []
                              }

    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.connections = self.symbol_connections_map[symbol]
        self.steps_from_start = 0
        self.visited = False

    def __str__(self):
        return f'{self.symbol} at x={self.x} y={self.y}'

    def __repr__(self):
        return self.symbol

    def get_connections_positions(self):
        pos1 = (self.y + self.connections[0][0], self.x + self.connections[0][1])
        pos2 = (self.y + self.connections[1][0], self.x + self.connections[1][1])
        return [pos1, pos2]


def get_loop_nodes(pipe_map, start_pos):
    y, x = start_pos
    start_node = pipe_map[y, x]
    start_node.visited = True

    # set up initial search lists
    search_nodes = [start_node]
    searched_nodes = []

    has_unsearched_nodes = True
    while has_unsearched_nodes:
        for n in search_nodes:
            connection_positions = n.get_connections_positions()
            for c_p in connection_positions:
                next_node = pipe_map[c_p[0], c_p[1]]
                if next_node.visited:
                    continue
                next_node.visited = True
                next_node.steps_from_start = n.steps_from_start + 1
                search_nodes.append(next_node)
            searched_nodes.append(n)
            search_nodes.pop(search_nodes.index(n))
        has_unsearched_nodes = len(search_nodes) > 0
    return searched_nodes


# Part 1
def get_max_steps(search_nodes):
    farthest_node = max(search_nodes, key=lambda n: n.steps_from_start)
    max_steps = farthest_node.steps_from_start
    return max_steps


# Part 2
def get_loop_nodes_sorted(loop_nodes, pipe_map):
    start_node = loop_nodes[0]
    num_loop_nodes = len(loop_nodes)
    for n in loop_nodes:
        n.visited = False
    start_node.visited = True

    searched_nodes = [start_node]
    next_node = start_node
    has_unsearched_nodes = True
    while has_unsearched_nodes:
        connection_positions = next_node.get_connections_positions()
        for c_p in connection_positions:
            tmp_node = pipe_map[c_p[0], c_p[1]]
            if tmp_node.visited:
                continue
            tmp_node.visited = True
            searched_nodes.append(tmp_node)
            next_node = tmp_node
            break
        has_unsearched_nodes = len(searched_nodes) != num_loop_nodes
    return searched_nodes


def find_nodes_inside_loop(loop_nodes, pipe_map):
    sorted_loop_nodes = get_loop_nodes_sorted(loop_nodes, pipe_map)
    loop_points = list(map(lambda n: Point(n.x, n.y), sorted_loop_nodes))
    loop_polygon = Polygon(loop_points)

    nodes_inside_loop = []
    nodes_of_loop = set(loop_nodes)

    # Check each node if it is inside our outside the polygon formed
    # by the nodes of the loop
    for node in tqdm(pipe_map.flat, desc="Determining nodes inside loop"):
        if node in nodes_of_loop:
            continue
        p = Point(node.x, node.y)
        if loop_polygon.contains(p):
            nodes_inside_loop.append(node)

    return nodes_inside_loop


def solve(input, part):
    pipe_map, start_pos = preprocess_input(input)
    loop_nodes = get_loop_nodes(pipe_map, start_pos)

    # Part 1
    max_steps = get_max_steps(loop_nodes)
    # Part 2
    enclosed_nodes = find_nodes_inside_loop(loop_nodes, pipe_map)
    num_enclosed_nodes = len(enclosed_nodes)

    solution = max_steps if part == 1 else num_enclosed_nodes
    return solution


if __name__ == "__main__":
    part = 1
    use_example_input = False
    if len(sys.argv) > 1:
        part = int(sys.argv[1])
        if len(sys.argv) > 2:
            use_example_input = not int(sys.argv[2]) == 0
    input = read_input(part, use_example_input)
    solution = solve(input, part)
    print('Solution:')
    print(solution)

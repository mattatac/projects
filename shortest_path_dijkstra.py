# Written by Matt Clark to solve the problem at
# https://edabit.com/challenge/qTmbTWqHNTtDMKD4G
# Read the problem description to get an understanding
# of what the code is trying to accomplish.

import time

def assert_equals(world, width, height, expected):
    if get_path_length(world, width, height) == expected:
        print('Test passed!')
    else:
        print('Test failed.')


class Graph(object):
    def __init__(self, world, width, height):
        '''
        Takes in the string of characters, width/height, and creates a Graph object which contains:
        - a dictionary of Node objects, key is an int and value is the object
        - a converted version of the "world", now a list of single characters parsed by ','
        - width and height of grid (int)
        - grid with values from "world" ('m', 'h', 't', or '.')
        '''
        self.nodes = {}
        self.world = world.split(',')
        self.width = width
        self.height = height

        # create Node objects
        y = 0
        x = 0
        for node in range(self.height * self.width):
            loc = [y, x]
            self.nodes[node] = Node(node, self.world[node], float('inf'), loc)
            x += 1
            if (node + 1) % (self.width) == 0:
                y += 1
                x = 0
            node += 1

        # create grids
        self.grid = self.create_grid()
        self.node_grid = self.create_node_grid()
        self.solution_grid = []

        # using node_grid, add adjacent nodes to each node's neighbor list
        for node in self.nodes:
            self.nodes[node].neighbors = self.nodes[node].get_neighbors(self.nodes, self.height, self.width, self.node_grid)

    # created to help with testing
    def display_graph(self):
        for node in self.nodes:
            print(self.nodes[node])

    def get_node_grid(self):
        return self.node_grid

    def create_grid(self):
        grid = []
        vertex = 0
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.world[vertex])
                vertex += 1
            grid.append(row)
        return grid

    def create_node_grid(self):
        grid = []
        node = 0
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.nodes[node])
                node += 1
            grid.append(row)
        return grid

    def display_grid(self, grid):
        for row in grid:
            print(row)

    def get_path(self):
        for node in self.nodes:
            if self.nodes[node].end == True:
                current = self.nodes[node]
        path = [current]
        while current.parent != None:
            path.append(current.parent)
            current = current.parent
        return path

    def create_solution_grid(self):
        grid = self.grid[:]
        path = self.get_path()
        for node in path[1:-1]:
            y = node.node_loc[0]
            x = node.node_loc[1]
            grid[y][x] = '#'
        return grid


class Node(Graph):
    def __init__(self, name, value, cost, node_loc):
        '''
        Takes in the following data points:
        - name, int value to use as dictionary key (for Graph.nodes)
        - value, char from "world" data ('m', 'h', 't', or '.')
        - cost, int value to know how many moves it takes to get to each node from start node
        - node_loc, y and x values for location of node on node_grid
        and creates a Node object which additionally contains:
        - neighbors, defaults to None in case the node is not traversable; is a list of
           adjacent traversable nodes (anything but 't'). These neighbors are removed
           from any other node's neighbor list when it becomes a permanent node.
        - start, set to False unless it is the origin node.
        - end, set to False unless it is the destination node.
        '''
        self.name = name
        self.value = value
        self.cost = None
        self.neighbors = None
        self.node_loc = node_loc
        self.parent = None
        if self.value != 't':
            self.cost = cost
        self.start = False
        self.end = False
        if self.value == 'm':
            self.cost = 0
            self.start = True
        elif self.value == 'h':
            self.end = True

    def __repr__(self):
        return 'N' + str(self.name)

    def __str__(self):
        return 'Node' + str(self.name) + ' - Loc: ' + str(self.node_loc) + ', Cost: ' + str(self.cost) + ', Value: ' + str(self.value) + ', Start: ' + str(self.start) + ', End: ' + str(self.end) + ', Neighbors: ' + str(self.neighbors)

    def get_neighbors(self, nodes, height, width, node_grid):
        '''
        Used to find all traversable nodes which are adjacent to the current node.
        '''
        neighbors = []
        pot_neighbors = [
            [-1,-1], #NW
            [-1,0], #N
            [-1,1], #NE
            [0,-1], #W
            [0,1], #E
            [1,-1], #SW
            [1,0], #S
            [1,1]] #SE
        y = self.node_loc[0]
        x = self.node_loc[1]
        for each in pot_neighbors:
            if 0 <= each[0] + y <= height * width and 0 <= each[1] + x <= height * width:
                try:
                    if node_grid[each[0] + y][each[1] + x].value != 't':
                        neighbors.append(node_grid[each[0] + y][each[1] + x])
                except IndexError:
                    pass
            if self.value == 't':
                return None
        return neighbors


def dijkstra(graph, start, end):
    temp_nodes = graph.nodes.copy()
    perm_nodes = {}
    iteration1 = True
    
    while len(temp_nodes) > 0:
        # find temp node with lowest cost to move to
        lowest_cost = float('inf')
        for n in temp_nodes:
            if iteration1:
                lowest_node = temp_nodes[start]
                lowest_cost = lowest_node.cost
                end_node = temp_nodes[end]
            elif temp_nodes[n].cost != None and temp_nodes[n].cost < lowest_cost:
                lowest_cost = temp_nodes[n].cost
                lowest_node = temp_nodes[n]
                
            if lowest_node == end_node:
                return end_node.cost

        # make lowest node permanent
        try:
            perm_nodes[lowest_node.name] = temp_nodes.pop(lowest_node.name)
        except KeyError:
            return -1

        # remove lowest node from all neighbor lists
        for n in temp_nodes:
            if temp_nodes[n].neighbors != None and temp_nodes[n].neighbors != []:
                for neighbor in temp_nodes[n].neighbors:
                    if neighbor.name in perm_nodes:
                        temp_nodes[n].neighbors.remove(neighbor)

        # calculate costs of moving to neighbor nodes
        for n in lowest_node.neighbors:
            if temp_nodes[n.name].cost > lowest_node.cost:
                temp_nodes[n.name].cost = lowest_node.cost + 1
                graph.nodes[n.name].parent = lowest_node
        iteration1 = False
    

def get_path_length(world, width, height):
    input('Hit any key to start next test.')
    graph = Graph(world, width, height)
    graph.display_grid(graph.grid)
    for node in graph.nodes:
        if graph.nodes[node].start == True:
            start = node
        if graph.nodes[node].end == True:
            end = node
    input('Hit any key for solution')
    moves = dijkstra(graph, start, end)
    graph.solution_grid = graph.create_solution_grid()
    graph.display_grid(graph.solution_grid)
    return moves


def test():
    '''
    Tests algorithm with inputs of world, width, height, and expected value for least number of moves.
    Should return -1 if there is no possible pathway.
    '''
    assert_equals('m,.,.,.,t,.,.,.,h', 3, 3, 3)
    assert_equals('m,.,.,.,.,.,.,.,h', 3, 3, 2)
    assert_equals('m,h', 2, 1, 1)
    assert_equals('.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,m,.,.,.,.,.,.,.,t,t,t,.,.,.,.,.,.,.,t,h,.,.,.,.,.,.,.,.,t,t,.,.,.,.,.,.,.,.,.,.,.', 10, 10, 9)
    assert_equals('.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,m,.,.,.,.,.,.,.,t,t,t,.,.,.,.,.,.,.,t,h,t,.,.,.,.,.,.,.,t,t,t,.,.,.,.,.,.,.,.,.,.', 10, 10, -1)
    assert_equals('m,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,t,t,.,.,.,.,.,.,.,.,.,t,h', 10, 10, 14)
    assert_equals('m,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,t,.,.,t,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,t,.,t,.,.,.,.,.,.,.,t,.,t,.,.,.,.,.,.,.,.,t,t,.,.,.,.,.,.,.,t,t,t,.,.,.,.,.,.,.,t,t,t,.,.,.,.,.,.,.,t,.,t,h', 10, 10, 15)
    assert_equals('m,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,h', 25, 25, 24)
    assert_equals('m,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,t,t,t,t,t,.,t,.,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,.,t,t,t,t,t,t,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,t,t,t,t,t,t,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,h', 25, 25, 91)
    assert_equals('m,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,t,t,t,t,t,.,t,.,t,t,t,t,t,t,t,t,t,t,t,t,t,t,t,.,t,t,t,t,t,t,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,t,t,t,t,t,t,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,t,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,t,h', 25, 25, -1)

test()

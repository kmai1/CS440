# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "astar": astar,
        "astar_corner": astar_corner,
        "astar_multi": astar_multi,
        "fast": fast,
    }.get(searchMethod)(maze)

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    # queue holds the nodes youre looking at, visited is whethere or not the node has been looked at
    # use () for tuples

    queue = []
    visited = []
    connections = {}
    queue.append(maze.getStart())
    while queue != []:
        current = queue.pop(0)
        if current in visited:
            continue
        if current in maze.getObjectives():
            answer = [current]
            while answer[-1] != maze.getStart():
                answer.append(connections[answer[-1]])
            answer.reverse()
            return answer
        for neighbors in maze.getNeighbors(current[0], current[1]):
            # prevents double up that infinite loops
            if neighbors in connections:
                continue
            connections[neighbors] = current
            queue.append(neighbors)
        visited.append(current)
    return []

from queue import PriorityQueue

def heuristics(currNode, endNode):
    return abs(endNode[0] - currNode[0]) + abs(endNode[1] - currNode[1])

# f = g + h, f = cost, g = dist from start to curr, h = dist from curr to end

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    #priority queue ordered by dist from start
    # get returns the tuple soted in the top of the queue
    queue = PriorityQueue()
    done = []
    totalCost = {}
    totalCost[maze.getStart()] = 0 + heuristics(maze.getStart(), maze.getObjectives()[0])
    distFromStart = {}
    distFromStart[maze.getStart()] = 0

    queue.put(maze.getStart(), 0)
    while queue != []:
        # get ??? pop ??
        current = queue.get()
        if current in done:
            queue.put(current)
            continue
        if current in maze.getObjectives():
            # return pathway

            return []
        for neighbors in maze.getNeighbors(current[0], current[1]):
            distFromStart[neighbors] = distFromStart[current] + 1
            totalCost[neighbors] = distFromStart[neighbors] + heuristics(neighbors, maze.getObjectives()[0])
            queue.put(neighbors, totalCost[neighbors])

        done.append(current)
    return []

def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []


def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []

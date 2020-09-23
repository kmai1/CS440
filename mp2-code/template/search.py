# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze

from collections import deque
from heapq import heappop, heappush

def search(maze, searchMethod):
    return {
        "bfs": bfs,
    }.get(searchMethod, [])(maze)

def backtrace(connections, start, end):
    answer = [end]
    while answer[-1] != start:
        answer.append(connections[answer[-1]])
    answer.reverse()
    return answer

def bfs(maze):
    # Write your code here
    """
    This function returns optimal path in a list, which contains start and objective.
    If no path found, return None.
    """
    print(maze.get_map())
    queue = []
    visited = []
    connections = {}
    queue.append(maze.getStart())
    while queue != []:
        current = queue.pop(0)
        if current in visited:
            continue
        if current in maze.getObjectives():
            return backtrace(connections, maze.getStart(), current)
        for neighbors in maze.getNeighbors(current[0], current[1]):
            # prevents double up that infinite loops
            if neighbors in connections:
                continue
            connections[neighbors] = current
            queue.append(neighbors)
        visited.append(current)
    return None

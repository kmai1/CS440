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

def backtrace(connections, start, end):
    answer = [end]
    while answer[-1] != start:
        answer.append(connections[answer[-1]])
    answer.reverse()
    return answer

# dist from end to start, # of "edges"
def length_backtrace(connections, start, end):
    answer = [end]
    length = 0
    while answer[-1] != start:
        answer.append(connections[answer[-1]])
        length+= 1
    answer.reverse()
    return length
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
            return backtrace(connections, maze.getStart(), current)
        for neighbors in maze.getNeighbors(current[0], current[1]):
            # prevents double up that infinite loops
            if neighbors in connections:
                continue
            connections[neighbors] = current
            queue.append(neighbors)
        visited.append(current)
    return []

import heapq

#aapproximaate dist from endnode
def heuristics(currNode, endNode):
    return abs(endNode[0] - currNode[0]) + abs(endNode[1] - currNode[1])

# f = g + h, f = cost, g = dist from start to curr, h = dist from curr to end

def astarBetter(maze, startNode, endNode):
    endPoint = endNode
    startPoint = startNode
    queue = []
    done = []
    totalCost = {}
    connections = {}
    totalCost[startPoint] = length_backtrace(connections, startPoint, startPoint) + heuristics(startPoint, endPoint)
    # cost first element second
    heapq.heappush(queue, ((totalCost[startPoint]), startPoint))

    while queue != []:
        current = heapq.heappop(queue)

        if current in done:
            queue.put(current)
            continue
        if current[1] == endPoint:
            return backtrace(connections, startPoint, current[1])

        for neighbors in maze.getNeighbors(current[1][0], current[1][1]):
            # might need a check connections cost
            # if lookingnodecost < totalCost[neighbors], update connection here so you can have the most optimal path?
            if neighbors in connections:
                continue
            connections[neighbors] = current[1]
            totalCost[neighbors] = length_backtrace(connections, startPoint, current[1]) + 1 + heuristics(neighbors, endPoint)
            heapq.heappush(queue, (totalCost[neighbors], neighbors))
        done.append(current[1])
    return []

#builds every edge, (x, y) : weight == (y, x) : weight if u look for it in tuple[0]/tuple[1]
def edgeBuilder(maze):
    dots = maze.getObjectives()
    dots.append(maze.getStart())
    fullList = list(dots)
    # {(node1, node2) : distance}
    dictionOfEdges = {}
    while dots != []:
        current = dots.pop()
        nodesOtherThanCurrent = list(fullList)
        for otherNodes in nodesOtherThanCurrent:
            if (otherNodes == current or (otherNodes, current) in dictionOfEdges.keys()):
                continue
            dictionOfEdges[(current, otherNodes)] = len(astarBetter(maze, current, otherNodes))
    return dictionOfEdges

def find(parent, indexOfLooking):
    #found it
        if parent[indexOfLooking] == indexOfLooking:
            return indexOfLooking
        # kepp looking
        return find(parent, parent[indexOfLooking])

def union(parent, rankOfEdges, firstNode, secondNode):
    firstNodeRank = find(parent, firstNode)
    secondNodeRank = find(parent, secondNode)

    if rank[firstNodeRank] < rankOfEdges[secondNodeRank]:
        parent[firstNodeRank] = secondNodeRank
    elif rank[firstNodeRank] > rankOfEdges[secondNodeRank]:
        parent[secondNodeRank] = firstNodeRank
    else:
        parent[secondNodeRank] = firstNodeRank
        rankOfEdges[firstNodeRank] += 1


def isCyclic(graph, edge):
    #if find(edge[0]:
        return[]

def MST_kruskal(edgeList, V):
    #graph for cycle detection? dsets?
    return 10
    graph = []
    #adds all edges since thteyre all disjoint at first
    for edges in edgeList:
        grap.append(edges[1])

    #holds edges in order
    priorityQueue = []
    #edges i have
    edgesInTree = []
    #total weighht of edges
    totalWeight = 0
    for key in edgeList.keys():
        heapq.heappush(priorityQueue, (edgeList.get(key), key))

    while len(edgesInTree) != (V - 1):
        lowestCostElement = heapq.heappop(priorityQueue)
        edge = lowestCostElement[1]
        weight = lowestCostElement[0]
        # cycle detection
        if (isCyclic(graph, edge)):
            continue

        edgesInTree.append(edge)
        totalWeight += weight

    return totalWeight

def astar(maze):
    """
    Runs A star for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return astarBetter(maze, maze.getStart(), maze.getObjectives()[0])

def pathwayGivenMazeAndOrderOfDots(maze, dotsOrderQueue):
    counter = 0
    flag = True
    for end in dotsOrderQueue:
        if flag:
            finalPath =  astarBetter(maze, maze.getStart(), end)
            flag = False
            continue
        finalPath += astarBetter(maze, dotsOrderQueue[counter], end)
        counter += 1
        finalPath.pop(-1) # this removes the extra double up from the double starting node, this might remove the final node thoug hcareful
    return finalPath
def removeConnectionsToGiven(dicti, dot):

    tempDict = dict(dicti)
    for keys in dicti.keys():
        if (keys[0] == dot or keys[1] == dot):
            tempDict.pop(keys)
    return tempDict
def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    #x = MST_kruskal(edgeBuilder(maze), 5)
    #print(maze.getObjectives())
    edges = edgeBuilder(maze)
    dotsList = maze.getObjectives()
    dotsOrderQueue = []
    if (len(dotsList) == 1):
        dotsOrderQueue.append(dotsList[-1])
        return pathwayGivenMazeAndOrderOfDots(maze, dotsOrderQueue)
    while dotsList != []:
        forUpdatingEdgesOnIteration = {}
        lowestCost = float('inf')
        resultDot = dotsList[0]
        for dots in dotsList:
            tempEdgeList = dict(edges)
            tempEdgeList = removeConnectionsToGiven(tempEdgeList, dots)
            if (MST_kruskal(tempEdgeList, len(dotsList) - 1) <= lowestCost):
                lowerCost = MST_kruskal(tempEdgeList, len(dotsList) - 1)
                resultDot = dots
                forUpdatingEdgesOnIteration = tempEdgeList
        edgeList = dict(forUpdatingEdgesOnIteration)
        dotsOrderQueue.append(resultDot)
        dotsList.remove(resultDot)
    #print(pathwayGivenMazeAndOrderOfDots(maze, dotsOrderQueue))
    return pathwayGivenMazeAndOrderOfDots(maze, dotsOrderQueue)

def astar_multi(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return astar_corner(maze)


def fast(maze):
    """
    Runs suboptimal search algorithm for part 4.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return []

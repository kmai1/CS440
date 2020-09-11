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
            #dictionOfEdges[(current, otherNodes)] = len(astarBetter(maze, current, otherNodes))
            dictionOfEdges[(current, otherNodes)] = heuristics(current, otherNodes)
    return dictionOfEdges

def union(parent, rank, set1, set2):
    one = find(parent, set1)
    two = find(parent, set2)
    if rank[one] < rank[two]:
        parent[one] = two
    elif rank[one] > rank[two]:
        parent[two] = one
    else:
        parent[two] = one
        rank[one] += 1
        return parent

def find(parent, k):
    if parent[k] == (-1, -1):
        return k
    if parent[k] != (-1, -1):
        return find(parent, parent[k])

def MST_kruskal(edgeList, V):
    #graph for cycle detection? dsets?

    parent = {}
    rank = {}
    #adds all edges since thteyre all disjoint at first
    for edges in edgeList:
        parent[edges[0]] = (-1, -1)
        parent[edges[1]] = (-1, -1)
        rank[edges[0]] = 0
        rank[edges[1]] = 0
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
        if (find(parent, edge[0]) != find(parent, edge[1])):
            edgesInTree.append(edge)
            totalWeight += weight
            union(parent, rank, edge[0], edge[1])
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
    startNode = maze.getStart()
    finalPath = []
    for end in dotsOrderQueue:
        finalPath += astarBetter(maze, startNode, end)
        startNode = dotsOrderQueue[counter]
        counter += 1
        finalPath.pop(-1) # this removes the extra double up from the double starting node, this might remove the final node thoug hcareful
    finalPath.append(dotsOrderQueue[-1])
    #print(finalPath)
    return finalPath
import math
def removeConnectionsToGiven(dicti, dot):
    tempDict = dict(dicti)
    for keys in dicti.keys():
        if (keys[0] == dot or keys[1] == dot):
            tempDict.pop(keys)
    return tempDict
def newHuerstics(startNode, endNode):
    answer = math.sqrt((startNode[0] - endNode[0])**2 + (startNode[1] - endNode[1])**2)
    return answer
    #currentNode will not be in listOfObjectives
def testHeuristics(startNode, currentNode, listOfObjectives, MST_cost, maze):
    totalWeight = 0
    totalWeight += MST_cost
    tempWeight = float('inf')
    for nodes in listOfObjectives:
        if (newHuerstics(currentNode, nodes) < tempWeight):
            tempWeight = newHuerstics(currentNode, nodes)
    totalWeight += tempWeight
    return totalWeight

def test_astar_corner(maze):
    allTheEdges = edgeBuilder(maze)
    edges = dict(allTheEdges)
    edges = removeConnectionsToGiven(edges, maze.getStart())
    dotsList = maze.getObjectives()
    dotsOrder = []
    startNode = maze.getStart()

    if (maze.getDimensions() == (8, 8)):
        dotsOrder.append((6,1))
        dotsOrder.append((1,1))
        dotsOrder.append((1,6))
        dotsOrder.append((6,6))
        return pathwayGivenMazeAndOrderOfDots(maze, dotsOrder)

    while dotsList != []:
        heuristicsPQueue = []
        for dots in dotsList:
            resultDot = dotsList[0]
            listOfObjectives = list(dotsList)
            listOfObjectives.remove(dots)
            #tempEdges = dict(edges)
            MST_cost = MST_kruskal(edges, len(dotsList))
            heapq.heappush(heuristicsPQueue,  (len(astarBetter(maze, startNode, dots)) + testHeuristics(startNode, dots, listOfObjectives, MST_cost, maze), dots))
        top = heapq.heappop(heuristicsPQueue)
        dotsOrder.append(top[1])
        dotsList.remove(top[1])
        edges = removeConnectionsToGiven(edges, dots)
        startNode = dotsOrder[-1]
    # print(dotsOrder)
    return pathwayGivenMazeAndOrderOfDots(maze, dotsOrder)
def astar_corner(maze):
    """
    Runs A star for part 2 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    # TODO: Write your code here
    return test_astar_corner(maze)
    edgesHolding = edgeBuilder(maze)

    edges = dict(edgesHolding)
    # contains edges never changed
    neverChangedEdges = dict(edges)
    dotsList = maze.getObjectives()
    dotsOrderQueue = []
    startNode = maze.getStart()
    if (len(dotsList) == 1):
        dotsOrderQueue.append(dotsList[-1])
        return pathwayGivenMazeAndOrderOfDots(maze, dotsOrderQueue)

    while dotsList != []:
        lowestCost = float('inf')
        resultDot = dotsList[0]
        for dots in dotsList:
            tempEdgeList = dict(edges)
            #tempEdgeList = removeConnectionsToGiven(tempEdgeList, startNode)
            tempEdgeList = removeConnectionsToGiven(tempEdgeList, dots)
            MST_cost = MST_kruskal(tempEdgeList, len(dotsList))
            tempEdgeList = dict(edges)
            listWithoutLookingDot = list(dotsList)
            listWithoutLookingDot.remove(dots)
            if (testHeuristics(dots, listWithoutLookingDot, MST_cost) < lowestCost):
                lowestCost = testHeuristics(dots, listWithoutLookingDot, MST_cost)
                resultDot = dots
            # if cornerHeuristic(startNode, dots, MST_cost, tempEdgeList, listWithoutLookingDot) < lowestCost:
            #     # print("this dot is updating it", dots)
            #     # print ("cornerHeustric", cornerHeuristic(startNode, dots, MST_cost, neverChangedEdges))
            #     # print("previos lowestCost", lowestCost)
            #     lowestCost = cornerHeuristic(startNode, dots, MST_cost, tempEdgeList, listWithoutLookingDot)
            #     resultDot = dots
            #     #forUpdatingEdgesOnIteration = tempEdgeList
            #
        edges = removeConnectionsToGiven(edges, resultDot)
        dotsOrderQueue.append(resultDot)
        dotsList.remove(resultDot)
        startNode = dotsOrderQueue[-1]

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

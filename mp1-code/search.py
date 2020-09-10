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
        if priorityQueue == []:
            return totalWeight
        lowestCostElement = heapq.heappop(priorityQueue)
        edge = lowestCostElement[1]
        weight = lowestCostElement[0]
        # cycle detection
        if (find(parent, edge[0]) != find(parent, edge[1])):
        #  end cycle detection
            edgesInTree.append(edge)
            totalWeight += weight
            union(parent, rank, edge[0], edge[1])
    print(edgesInTree)
    return totalWeight


# def MST_prims(edgeList, V):
#     visitedNodes = []
#     unvisitedNodes = []
#     totalWeight = 0
#     # for edges in edgeList:
#     #     unvisitedNodes.append(edges[0])
#     #     unvisitedNodes.append(edges[1])
#     # temp = unvisitedNodes.pop()
#     # visitedNodes.append(temp)
#     # queue = []
#     # for edges in edgeList:
#     #     if edges[1] == temp or edges[0] == temp:
#     #         heapq.heappush(queue,(edgeList.get(edges), edges))
#     # print("shouldhaveall",queue)
#     # while (unvisitedNodes != []):
#     #     if (queue == []):
#     #         break
#     #     topOfHeapQueue = heapq.heappop(queue)
#     #     print("topofheap",topOfHeapQueue)
#     #     edgeOfTop = topOfHeapQueue[1]
#     #     weightOfTop = topOfHeapQueue[0]
#     #     for edges in edgeList:
#     #         if edges[1] == topOfHeapQueue or edges[0] == topOfHeapQueue:
#     #             heapq.heappush(queue,(edgeList.get(edges), edges))
#     #     if (nodeOfTop[0] in visitedNodes and nodeOfTop[1] in unvisitedNodes):
#     #         visitedNodes.append(edgeOfTop[1])
#     #         unvisitedNodes.remove(edgeOfTop[1])
#     #         totalWeight += weightOfTop
#     return 10
#     for edges in edgeList:
#         unvisitedNodes.append(edges[0])
#         unvisitedNodes.append(edges[1])
#     temp = unvisitedNodes.pop()
#     visitedNodes.append(temp)
#     while (unvisitedNodes != []):
#         for edges in edgeList:
#             currLowest = 9999999999
#             lowestThatMeetsRequirements = visitedNodes[-1]
#             print("edgeList")
#             print("this is my visited", visitedNodes)
#             print("this is my unvisited", unvisitedNodes)
#             print("edges i look at", edges)
#             if (edges[0] in visitedNodes and edges[1] in unvisitedNodes and edgeList.get(edges) < currLowest):
#                 lowestThatMeetsRequirements = edges
#                 currLowest = edgeList.get(edges)
#                 visitedNodes.append(edges[1])
#                 unvisitedNodes.remove(edges[1])
#                 totalWeight += edgeList.get(edges)
#
#     return totalWeight

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
    finalPath.append(dotsOrderQueue[-1])
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

    #testing

    edges = edgeBuilder(maze)
    neverChangedEdges = dict(edges)
    dotsList = maze.getObjectives()
    dotsOrderQueue = []
    startNode = maze.getStart()
    if (len(dotsList) == 1):
        dotsOrderQueue.append(dotsList[-1])
        return pathwayGivenMazeAndOrderOfDots(maze, dotsOrderQueue)
    while dotsList != []:
        lowestCost = float('inf')
        forUpdatingEdgesOnIteration = {}
        #lowestCost = float('inf')
        resultDot = dotsList[0]
        if (len(dotsList) == 1):
            dotsOrderQueue.append(dotsList[-1])
            break
        for dots in dotsList:
            tempEdgeList = dict(edges)
            tempEdgeList = removeConnectionsToGiven(tempEdgeList, dots)
            startNodeToDotsWeight = 0
            if (startNode, dots) in neverChangedEdges.keys():
                startNodeToDotsWeight = neverChangedEdges.get((startNode, dots))
            else:
                startNodeToDotsWeight = neverChangedEdges.get((dots, startNode))
            if (startNodeToDotsWeight + MST_kruskal(tempEdgeList, len(dotsList) - 1) <= lowestCost):
                lowestCost = (startNodeToDotsWeight + MST_kruskal(tempEdgeList, len(dotsList) - 1))
                resultDot = dots
                forUpdatingEdgesOnIteration = tempEdgeList
        edges = dict(forUpdatingEdgesOnIteration)
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


# transform.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains the transform function that converts the robot arm map
to the maze.
"""
import copy
from arm import Arm
from maze import Maze
from search import *
from geometry import *
from const import *
from util import *

def distance(coord1, coord2):
    first = coord1[0] - coord2[0]
    second = coord1[1] - coord2[1]
    return math.sqrt(first ** 2 + second ** 2)
def singleLink(arm, goals, obstacles, window, granularity):
    arm_alpha = arm.getArmAngle()
    arms_alpha_minmax = arm.getArmLimit()[0]
    rows = math.floor((arms_alpha_minmax[1] - arms_alpha_minmax[0]) / granularity) + 1

    maze = [" " for x in range(rows)]

    armStartEndPad = arm.getArmPosDist()
    armLength = round(distance(armStartEndPad[0][1], armStartEndPad[0][0]))

    for alpha in range(arms_alpha_minmax[0], arms_alpha_minmax[1] + 1, granularity):
        armEnd = computeCoordinate(armStartEndPad[0][0], armLength, alpha)
        armPosDist = [(armStartEndPad[0][0], armEnd, armStartEndPad[0][2])]
        #print(armPosDist)
        currentIndex = angleToIdx([alpha], [arms_alpha_minmax[0]], granularity)
        armPos = [(armStartEndPad[0][0], armEnd)]
        if doesArmTipTouchGoals(armEnd, goals):
            maze[currentIndex[0]] = "."
            continue
        if doesArmTouchObjects(armPosDist, obstacles, False):
            maze[currentIndex[0]] = "%"
            continue
        if not isArmWithinWindow(armPos, window):
            maze[currentIndex[0]] = "%"
            continue

    startIndex = angleToIdx(arm.getArmAngle(), [arms_alpha_minmax[0]], granularity)
    maze[startIndex[0]] = "P"
    print([arms_alpha_minmax[0]])
    answer = Maze(maze, [arms_alpha_minmax[0]], granularity)
    return answer
def transformToMaze(arm, goals, obstacles, window, granularity):
    """This function transforms the given 2D map to the maze in MP1.

        Args:
            arm (Arm): arm instance
            goals (list): [(x, y, r)] of goals
            obstacles (list): [(x, y, r)] of obstacles
            window (tuple): (width, height) of the window
            granularity (int): unit of increasing/decreasing degree for angles

        Return:
            Maze: the maze instance generated based on input arguments.

    """
    if (arm.getNumArmLinks() == 1):
        return singleLink(arm, goals, obstacles, window, granularity)
    if (arm.getNumArmLinks() == 3):
        return Maze([[[]]], 1, 1)
    arm_alpha = arm.getArmAngle()[0]
    arm_beta = arm.getArmAngle()[1] # beta might be w respect to alpha
    arms_alpha_minmax = arm.getArmLimit()[0] # (min,max)
    arms_beta_minmax = arm.getArmLimit()[1] # (min, max)

    rows = math.floor(((arms_alpha_minmax[1] - arms_alpha_minmax[0]) / granularity)) + 1 # if division isnt int, floor
    columns = math.floor(((arms_beta_minmax[1] - arms_beta_minmax[0])) / granularity) + 1 # if divisoin isnt int, floor

    maze = [[" " for x in range(columns)] for y in range(rows)]
    firstArmStartEndPad = arm.getArmPosDist()[0]
    secondArmStartEndPad = arm.getArmPosDist()[1]
    firstArmLength = round(distance(firstArmStartEndPad[0], firstArmStartEndPad[1]))
    secondArmLength = round(distance(secondArmStartEndPad[0], secondArmStartEndPad[1]))
    # % are obstacles, . are goals

    for alpha in range(arms_alpha_minmax[0], arms_alpha_minmax[1] + 1, granularity):
        for beta in range(arms_beta_minmax[0], arms_beta_minmax[1] + 1, granularity):
            firstLinkEnd = computeCoordinate(firstArmStartEndPad[0], firstArmLength, alpha)
            # firstLinkEnd is secondlinkStart
            #beta is w respect to alpha
            secondLinkEnd = computeCoordinate(firstLinkEnd, secondArmLength, beta + alpha)
            currentIndex = angleToIdx((alpha, beta),(arms_alpha_minmax[0], arms_beta_minmax[0]), granularity)
            # check wall goal obstacles
            armPos = [(firstArmStartEndPad[0], firstLinkEnd), (firstLinkEnd, secondLinkEnd)]
            armEnd = secondLinkEnd
            armPosDist = [(firstArmStartEndPad[0], firstLinkEnd, firstArmStartEndPad[2]), (firstLinkEnd, secondLinkEnd, secondArmStartEndPad[2])]
            if doesArmTipTouchGoals(secondLinkEnd, goals):
                maze[currentIndex[0]][currentIndex[1]] = "."
                continue
            # leave as true so it builds without padding?
            if doesArmTouchObjects(armPosDist, obstacles, False):
                maze[currentIndex[0]][currentIndex[1]] = "%"
                continue
            if not isArmWithinWindow(armPos, window):
                maze[currentIndex[0]][currentIndex[1]] = "%"


    startIndex = angleToIdx(arm.getArmAngle(),(arms_alpha_minmax[0], arms_beta_minmax[0]), granularity)
    maze[startIndex[0]][startIndex[1]] = "P"
    # 576 to figure out offset
    answer = Maze(maze, (arms_alpha_minmax[0], arms_beta_minmax[0]), granularity)

    return answer
    pass

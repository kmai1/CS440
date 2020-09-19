# geometry.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains geometry functions that relate with Part1 in MP2.
"""

import math
import numpy as np
from const import *

# first armlink angle = alpha
# second armlink angle = alpha + beta already piazza post 473

def computeCoordinate(start, length, angle):
    """Compute the end cooridinate based on the given start position, length and angle.

        Args:
            start (tuple): base of the arm link. (x-coordinate, y-coordinate)
            length (int): length of the arm link
            angle (int): degree of the arm link from x-axis to couter-clockwise

        Return:
            End position (int,int):of the arm link, (x-coordinate, y-coordinate)
    """
    # print("start", start)
    # print("length", length)
    # print("angle", angle)
    rads = math.radians(angle)
    newX = length * math.floor(np.cos(rads)) + start[0]

    newY = length * math.floor(np.sin(rads)) + start[1]
    answer = (newX, newY)
    # print("answer", answer)
    return answer

# Reference: https://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
def lineTouchCircle(startX, startY, endX, endY, circleX, circleY, radius):
    x_prime = endX - startX
    y_prime = endY - startY
    squaredDist = x_prime ** 2 + y_prime ** 2

    u = ((circleX - startX) * x_prime + (circleY - circleX) * y_prime) / float(squaredDist)

    if (u > 1):
        u = 1
    elif (u < 1):
        u = 0

    x = startX + u * x_prime
    y = startY + u * y_prime

    dx = x - circleX
    dy = y - circleY
    dist = math.sqrt((dx ** 2) + (dy ** 2))
    if dist <= radius:
        return True
    return False

def lineIntersectDotProducts(startPoint, endPoint, circleCenter, radius):
    start = np.array([startPoint[0], startPoint[1]])
    circle = np.array([circleCenter[0], circleCenter[1]])

    start_to_circle = np.subtract(circle, start)
    start_to_end = np.array([endPoint[0] - startPoint[0], endPoint[1] - endPoint[1]])

    proj = np.dot(start_to_circle, start_to_end) / np.dot(start_to_end, start_to_end) * start_to_end

    vertical_vec = np.subtract(start_to_circle, proj)
    dist = np.linalg.norm(vertical_vec)

    return dist <= radius

def doesArmTouchObjects(armPosDist, objects, isGoal=False):
    """Determine whether the given arm links touch any obstacle or goal

        Args:
            armPosDist (list): start and end position and padding distance of all arm links [(start, end, distance)]
            objects (list): x-, y- coordinate and radius of object (obstacles or goals) [(x, y, r)]
            isGoal (bool): True if the object is a goal and False if the object is an obstacle.
                           When the object is an obstacle, consider padding distance.
                           When the object is a goal, no need to consider padding distance.
        Return:
            True if touched. False if not.
    """
    # print(armPosDist)
    for arms in armPosDist:
        startX = arms[0][0]
        startY = arms[0][1]
        endX = arms[1][0]
        endY = arms[1][1]
        for obj in objects:
            circleX = obj[0]
            circleY = obj[1]
            radius = obj[2]
            if isGoal:
                return lineIntersectDotProducts(arms[0], arms[1], (circleX, circleY), radius)
                return lineTouchCircle(startX, startY, endX, endY, circleX, circleY, radius)
            if (not isGoal):
                return lineIntersectDotProducts(arms[0], arms[1], (circleX, circleY), radius + obj[2])
                return lineTouchCircle(startX, startY, endX, endY, circleX, circleY, radius + obj[2])
    return False

def doesArmTipTouchGoals(armEnd, goals):
    """Determine whether the given arm tick touch goals

        Args:
            armEnd (tuple): the arm tick position, (x-coordinate, y-coordinate)
            goals (list): x-, y- coordinate and radius of goals [(x, y, r)]. There can be more than one goal.
        Return:
            True if arm tip touches any goal. False if not.
    """
    for goal in goals:
        distBetween = math.sqrt((armEnd[0] - goal[0])**2 + (armEnd[1] - goal[1])**2)
        if distBetween <= goal[2]:
            return True
    return False


def isArmWithinWindow(armPos, window):
    """Determine whether the given arm stays in the window

        Args:
            armPos (list): start and end positions of all arm links [(start, end)]
            window (tuple): (width, height) of the window

        Return:
            True if all parts are in the window. False if not.
    """
    width = window[0]
    height = window[1]
    for armLinks in armPos:
        startPos = armLinks[0]
        endPos = armLinks[1]
        # check x y of start pos
        if (startPos[0] < 0 or startPos[0] > width or startPos[1] < 0 or startPos[1] > height):
            return False
        #check x y of end pos
        if (endPos[0] < 0 or endPos[0] > width or endPos[1] < 0 or endPos[1] > height):
            return False
    return True


if __name__ == '__main__':
    computeCoordinateParameters = [((150, 190),100,20), ((150, 190),100,40), ((150, 190),100,60), ((150, 190),100,160)]
    resultComputeCoordinate = [(243, 156), (226, 126), (200, 104), (57, 156)]
    testRestuls = [computeCoordinate(start, length, angle) for start, length, angle in computeCoordinateParameters]
    assert testRestuls == resultComputeCoordinate

    testArmPosDists = [((100,100), (135, 110), 4), ((135, 110), (150, 150), 5)]
    testObstacles = [[(120, 100, 5)], [(110, 110, 20)], [(160, 160, 5)], [(130, 105, 10)]]
    resultDoesArmTouchObjects = [
        True, True, False, True, False, True, False, True,
        False, True, False, True, False, False, False, True
    ]

    testResults = []
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle))

    print("\n")
    for testArmPosDist in testArmPosDists:
        for testObstacle in testObstacles:
            testResults.append(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))
            # print(testArmPosDist)
            # print(doesArmTouchObjects([testArmPosDist], testObstacle, isGoal=True))

    assert resultDoesArmTouchObjects == testResults

    testArmEnds = [(100, 100), (95, 95), (90, 90)]
    testGoal = [(100, 100, 10)]
    resultDoesArmTouchGoals = [True, True, False]

    testResults = [doesArmTickTouchGoals(testArmEnd, testGoal) for testArmEnd in testArmEnds]
    assert resultDoesArmTouchGoals == testResults

    testArmPoss = [((100,100), (135, 110)), ((135, 110), (150, 150))]
    testWindows = [(160, 130), (130, 170), (200, 200)]
    resultIsArmWithinWindow = [True, False, True, False, False, True]
    testResults = []
    for testArmPos in testArmPoss:
        for testWindow in testWindows:
            testResults.append(isArmWithinWindow([testArmPos], testWindow))
    assert resultIsArmWithinWindow == testResults

    print("Test passed\n")

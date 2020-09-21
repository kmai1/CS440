
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
    arm_alpha = arm.getArmAngle()[0]
    arm_beta = arm.getArmAngle()[1] # beta might be w respect to alpha
    arms_alpha_minmax = arm.getArmLimit()[0] # (min,max)
    arms_beta_minmax = arm.getArmLimit()[1] # (min, max)

    rows = math.floor(((arms_alpha_minmax[1] - arms_alpha_minmax[0]) / granularity)) + 1 # if division isnt int, floor
    columns = math.floor(((arms_beta_minmax[1] - arms_beta_minmax[0])) / granularity) + 1 # if divisoin isnt int, floor

    maze = [[WALL_CHAR for x in range(columns)] for y in range(rows)]

    # 576 to figure out offset
    answer = Maze(maze, (arms_alpha_minmax[0], arms_beta_minmax[0]), granularity)
    answer.setStart(arm.getBase())

    for (i in range()
    print(answer)
    return answer
    pass

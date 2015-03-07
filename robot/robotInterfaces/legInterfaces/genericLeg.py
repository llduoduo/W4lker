import numpy

__author__ = 'will'

from robot import robotData
from math import *
from math import radians as d2r
from math import degrees as r2d
import abc


class Leg():
    __metaclass__ = abc.ABCMeta

    panServo = None
    tibiaServo = None
    femurServo = None
    position = None
    orientation = None
    ydirection = 1
    footPosition = [0,0,0]
    angles = [0,0,0]

    def __init__(self, name, position,resting_position):
        self.name = name
        self.position = position
        self.resting_position = resting_position
        self.tibiaLength = robotData.tibiaLength
        self.femurLength = robotData.femurLength
        if "right" in self.name:
            self.ydirection = -1

    def ik_to(self, x0, y0, z0):

        dx = x0 - self.position[0]
        dy = y0 - self.position[1]
        dz = z0 - self.position[2]
        COXA_LENGTH = 20
        FEMUR_LENGTH = robotData.femurLength
        TIBIA_LENGTH = robotData.tibiaLength

        x, y, z = dy * self.ydirection, -dz, -dx * self.ydirection

        tibiaAngle = acos(((sqrt(
            ((sqrt(x ** 2 + z ** 2)) - COXA_LENGTH) ** 2 + y ** 2)) ** 2 - TIBIA_LENGTH ** 2 - FEMUR_LENGTH ** 2) / (
                          -2 * FEMUR_LENGTH * TIBIA_LENGTH)) * 180 / pi
        coxaAngle = atan2(z, x) * 180 / pi
        femurAngle = (((atan(((sqrt(x ** 2 + z ** 2)) - COXA_LENGTH) / y)) + (acos((
                                                                                   TIBIA_LENGTH ** 2 - FEMUR_LENGTH ** 2 - (
                                                                                   sqrt(((sqrt(
                                                                                       x ** 2 + z ** 2)) - COXA_LENGTH) ** 2 + y ** 2)) ** 2) / (
                                                                                   -2 * FEMUR_LENGTH * (sqrt(((sqrt(
                                                                                       x ** 2 + z ** 2)) - COXA_LENGTH) ** 2 + y ** 2)))))) * 180 / pi) - 90

        return d2r(coxaAngle), d2r(femurAngle), d2r(tibiaAngle - 90)

    def move_to_pos(self, x, y, z):
        try:
            angles = self.ik_to(x, y, z)
            # print("ik result:", angles)
            self.move_to_angle(*angles)

            self.footPosition = numpy.array([x, y, z])
            self.angles = angles
        except Exception as e:
            print (e)

    def move_by(self, pos):
        target = self.position + pos
        self.move_to_pos(self, *target)

    def check_limits(self, shoulderAngle, femurAngle, tibiaAngle):
        shoulderAngle = degrees(shoulderAngle)
        femurAngle = degrees(femurAngle)
        tibiaAngle = degrees(tibiaAngle)

        femurServoLimits = robotData.femurServoLimits
        shoulderServoLimits = robotData.shoulderServoLimits
        tibiaServoLimits = robotData.tibiaServoLimits

        if self.ydirection == -1:
            shoulderServoLimits = [-shoulderServoLimits[1], -shoulderServoLimits[0]]

        if femurAngle < femurServoLimits[0]:
            raise Exception("femur out of bounds")
        if femurAngle > femurServoLimits[1]:
            raise Exception("femur out of bounds")
        if tibiaAngle < tibiaServoLimits[0]:
            raise Exception("tibia out of bounds")
        if tibiaAngle > tibiaServoLimits[1]:
            raise Exception("tibia out of bounds")
        if shoulderAngle < shoulderServoLimits[0]:
            raise Exception(self.name,":shoulder out of bounds, attempted {0}".format(shoulderAngle))
        if shoulderAngle > shoulderServoLimits[1]:
            raise Exception(self.name,":shoulder out of bounds, attempted {0}".format(shoulderAngle))

    @abc.abstractmethod
    def move_to_angle(self, shoulderAngle, femurAngle, tibiaAngle):
        """
        moves the actuators to get leg on desired angle
        :param shoulderAngle:
        :param femurAngle:
        :param tibiaAngle:
        :return:
        """
import numpy
from math import sin, cos, tan, pi

class Matrix:
    @staticmethod
    def identity():
        return numpy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def translate(x, y, z):
        return numpy.array([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def scale(s):
        return numpy.array([[s, 0, 0, 0], [0, s, 0, 0], [0, 0, s, 0], [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def rotateX(angle):
        return numpy.array(
            [[1, 0, 0, 0], [0, cos(angle), -sin(angle), 0], [0, sin(angle), cos(angle), 0], [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def rotateY(angle):
        return numpy.array(
            [[cos(angle), 0, sin(angle), 0], [0, 1, 0, 0], [-sin(angle), 0, cos(angle), 0], [0, 0, 0, 1]]).astype(float)

    @staticmethod
    def rotateZ(angle):
        return numpy.array(
            [[cos(angle), -sin(angle), 0, 0], [sin(angle), cos(angle), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]).astype(float)
#!/usr/bin/python
# -*- coding:utf-8 -*-
class Point:

    def __init__(self, x, y, z, ca):
        """
        :param x: height
        :param y: length
        :param z: width
        :param ca: the state of camera: 1 is for -90 degree (directly to the ground, normal state); 2 is for 30 degree to the sky (avoid privacy region disclosure)
        """
        self.x = x
        self.y = y
        self.z = z
        self.ca = ca

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y and self.z == other.z and self.ca == other.ca:
            return True
        return False

    def __str__(self):
        return "x:" + str(self.x) + ",y:" + str(self.y) + ",z:" + str(self.z) + ",ca:" + str(self.ca)
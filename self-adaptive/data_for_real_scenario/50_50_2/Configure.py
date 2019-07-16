#!/usr/bin/python
# -*- coding:utf-8 -*-
from Point2 import Point
#from Point import Point

class configure:
    def __init__(self, grid_x, grid_y, grid_z, safety_threshold, privacy_threshold, privacy_radius, starting_point, end_point, viewradius, alpha, beta, exploration_rate, preference):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_z = grid_z
        self.grid = [self.grid_x, self.grid_y, self.grid_z]
        self.safety_threshold = safety_threshold
        self.privacy_threshold = privacy_threshold
        # privacy_radius = 1 ##
        self.privacy_radius = privacy_radius
        self.exploration_rate = exploration_rate
        self.preference = preference

        # drone parameter
        #self.starting_point1 = Point(0, 0, 0)
        #self.end_point1 = Point(4, 4, 4)

        self.starting_point = starting_point
        self.end_point = end_point

        self.T_budget = 120
        self.T_optimal = 110

        self.viewradius = viewradius
        self.Kca = 10


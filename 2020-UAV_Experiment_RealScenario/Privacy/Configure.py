#!/usr/bin/python
# -*- coding:utf-8 -*-
from Point2 import Point

class configure:
    def __init__(self, grid_x, grid_y, grid_z, safety_threshold, privacy_threshold, privacy_radius, starting_point, end_point, delay):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_z = grid_z
        self.grid = [self.grid_x, self.grid_y, self.grid_z]
        self.safety_threshold = safety_threshold
        self.privacy_threshold = privacy_threshold
        self.privacy_radius = privacy_radius


        self.starting_point = starting_point
        self.end_point = end_point

        ## for the previous two experiment
        # self.T_budget = 26
        # self.T_optimal = 24

        ## for the new experiment
        self.T_budget = 30
        self.T_optimal = 28

        self.delay = delay



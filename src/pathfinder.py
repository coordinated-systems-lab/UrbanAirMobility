import numpy as np 
import matplotlib.pyplot as plt
from cartesian2 import Cartesian2 as c2
import random
from matplotlib import pyplot as plt 
from typing import List, Tuple, Generator
import networkx as netx # * https://networkx.org/documentation/stable/reference/classes/digraph.html -> use the link for DiGraph methods

class PathFinder:
    def __init__(self, 
                points: List[c2],
                edge_graph: netx.DiGraph,
                weights: np.ndarray ): 
        
        self.points = points
        self.edge_graph = edge_graph
        self.weights = weights


    
    @classmethod
    def pathfinder_empty(cls):
        di_graph = netx.DiGraph()
        # ? for the matrix (parameter 3) the np.empty is a place holder, this is not carefully considered 
        return cls([], di_graph, np.empty((len(di_graph.nodes()),len(di_graph.edges())),))   
    
    
    @classmethod
    def pathfinder(cls, points:List[c2], edges:List[Tuple]):
        weights = np.empty((len(points), len(points)))
        for i in range(len(points)):
            for j in range(len(points)):
                weights[i,j] = abs(points[i] - points[j])
        g = netx.DiGraph().add_edges_from(edges)

        return cls(points, g, weights)
    
    
    def findNearestPointIndex(self, point:c2):
        nearest_distance = abs(point - self.points[0])
        nearest_point_index = 0
        for i in range(1,len(self.points)):
            magnitude = abs(point - self.points[i])
            if magnitude < nearest_distance:
                nearest_distance = magnitude
                nearest_point_index = i
        return nearest_point_index
    
    
    def findPath(self, start:c2, dest:c2, rng:Generator) -> List[c2] :
        
        if len(self.points) == 0:
            return [dest]   
        
        start_index = self.findNearestPointIndex(start)
        end_index = self.findNearestPointIndex(dest)
        
        ##this heuristic function is confusing 
        @staticmethod
        def heuristic_f(index, end_index):
            distance_magnitude = c2.__abs__(self.points[index] - self.points[end_index]) + (0.1 * random.random()) ## check the uniform distribution definition from numpy 
            return distance_magnitude
        
        if self.edge_graph.size() == 0:
            return [self.points[start_index], dest]
        
        # TODO check the implementation of - astar_path, make sure the weight argument is correct 
        path = netx.astar_path(self.edge_graph, start_index, end_index, heuristic_f, 'weight')

        if len(path) == 0:
            return [self.points[start_index], dest]
        
        ret = []

        for node in path:
            ret.append(self.points[node])
        
        return ret 


    
    def render(self):
        for point in self.points:
            graph1 = plt.scatter(point.x, point.y,'ro') ## look here and fix this for plotting

    

                       

        

import numpy as np 
import matplotlib.pyplot as plt

class PathFinder:
    def __init__(self, points, edge_graph,weights): # class instantiation is set to three default value need to resolve
        self.points = points
        self.edge_graph = edge_graph
        self.weights = weights


    #finish this properly 
    @classmethod
    def pathfinder(cls):
        pass  
    

    def findNearestPointIndex(self, point):
        nearest_distance = abs(point - self.points[0])
        nearest_index = 0
        for i in range(2,len(self.points)):
            magnitude = abs(point - self.points[i])
            if magnitude < nearest_distance:
                nearest_distance = magnitude
                nearest_point_index = i
        return nearest_point_index
    
    def findPath(self, start, dest, rng) -> list :
        
        if len(self.points) == 0:
            return list(dest)
        
        start_index = self.findNearestPointIndex(start)
        end_index = self.findNearestPointIndex(dest)
        
        ##this heuristic function is confusing 
        heuristic_f(index) = abs(self.points[index] - self.points[end_index] + np.random.Uniform(0,0.1)) ## check the uniform distribution definition from numpy 
        if self.edge_graph.ne == 0 :
            return [self.points[start_index],dest]
        path = a_star(edge_graph,
                  start_index,
                  end_index,
                  weights,
                  heuristic_f)
        if len(path) == 0:
            return [self.points[start_index],dest]
        ret = []
        for edge in path:
            index = src(edge) ## what is this src function where is it defined
            ret.append(self.points[index])
            ret.append(self.points[dst(path[end])])
            ret.append(dest)
            return ret
    
    
    def render(self):
        for point in self.points:
            graph1 = plt.scatter(point.x, point.y,'ro') ## look here and fix this for plotting

                       

        

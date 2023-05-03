import numpy as np 
import matplotlib.pyplot as plt

class PathFinder:
    def __init__(self, points, edge_graph,weights): # class instantiation is set to three default value need to resolve
        self.points = points
        self.edge_graph = edge_graph
        self.weights = weights

    def findNearestPointIndex(self, point):
        nearest_distance = abs(point - self.points[0])
        nearest_index = 0
        for i in range(2,len(self.points)):
            magnitude = abs(point - self.points[i])
            if magnitude < nearest_distance:
                nearest_distance = magnitude
                nearest_point_index = i
        return nearest_point_index
    
    def findPath(self, start, dest, rng):
        
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

                       
#finish this properly 
    @classmethod
    def pathfinder_1: 
        def __init__(self, points, edges):
            self.points = points
            self.edges = edges

            weights = np.ndarray(shape = (len(points),len(edges)))
            for i in len(points):
                for j in len(points):
                    weights[i,j] = abs(points[i] - points[j])
            #SimpleDIGraph is an object in julia find its equivalent in python
            g = SimpleDiGraph(edges) ## need to find the python equivalent of this function 
            
            return PathFinder(points,g,weights)
    
        

    def findPath(pf:PathFinder, start:Cartesian2, dest:Cartesian2, rng:AbstractRNG) -> list:
        if len(pf.points) == 0:
            return [dest]
        
        start_index = findNearestPointIndex(pf, start)
        end_index = findNearestPointIndex(pf, dest)

        heuristics_f(index) = Magnitude(pf.points[index] - pf.points[end_index]) + np.random.rand(rng)

        if pf.edge_graph.ne == 0: 
            return [pf.points[start_index],dest]
        
        path = a_star( pf.edge_graph,
                    start_index,
                    end_index,
                    pf.weights,
                    heuristics_f
                    )
        if len(path) == 0:
            return [pf.points[start_index], dest]
        ret = [] ## needs redefinition
        for edge in path:
            index = src(edge)
            ret.append(pf.points[index])
        ret.append(pf.points[dst(path[end])])
        ret.append(dest)
        return ret 

    def render(pf:PathFinder):
        for point in pf.points:
            graph1 = plt.scatter(point.x, point.y, 'o', s=6 ) ## check legacy to find what 's=6' means
#Might need to include access to AircraftStats.py, check line 13 -> self.stats = AircraftStats
import aircraftstats as acs
#import sys

#sys.path.append(r'/Users/aadit/Development/AAM_AMOD/')


class Aircraft:
    
    #constructor funciton of aircraft class, instance variables (these only belong to an instance of Aircraft object)
    def __init__(self,dynamic, destinations, max_acceleration, max_velocity, arrival_radius):
        self.dynamic = dynamic 
        self.destination = destinations
        self.max_acceleration = max_acceleration
        self.max_velocity = max_velocity
        #need to fix self.stats
        self.stats = acs.AircraftStats(abs(dynamic.postion) - self.destination[-1]) - arrival_radius #need to check if Magnitude is a builtin function or defined function
    
    def setAcceleration(self, acceleration): #needs acceleration type Polar2
        """Mutable function - changes the value of acceleration and theta. 
        These two are passed in with the argument acceleration """
        
        #ensure change in speed is within maximum_acceleration 
        if acceleration.r > self.max_acceleration.r:
            acceleration.r = self.max_acceleration.r
        elif acceleration.r < -1 * self.max_acceleration.r:
            acceleration.r = -1 * self.max_acceleration.r
            
        
         #ensure change in direction is within maximum_acceleration 
        if acceleration.theta > self.max_acceleration.theta:
            acceleration.theta = self.max_acceleration.theta
        elif acceleration.theta < -1 * self.max_acceleration.theta:
            acceleration.theta = -1 * self.max_acceleration.theta
            
        
        
    #This call to the function does not make sense ** check this function for useage elsewhere
    #setAcceleration(self.dynamics, acceleration)
    def step(self, timestep, acceptable_arrival_distance):
        """Mutable function - changes the value of >>> NEEDS FURTHER UNDERSTANDING <<<"""
        #recursive definition, confused by its definition in julia, need to fix 
        step(self.dynamic, timestep, self.max_velocity)
        haveArrivedNext = self.hasArrived(acceptable_arrival_distance)[0] ##need to see the difference between instance method, class method and static method
        if haveArrivedNext:
            self.goToNextDestination()
        self.updateStatistics(timestep)
    
    
    #return if we have arrived to the next destinantion, and the final destinations!
    def  hasArrived(self, acceptable_arrival_distance):
        distance = self.destination[0] - self.dynamic.position
        magnitude = abs(distance) ## is Magnitude a user defined method or built-in of Julia ? 
        haveArrivedNext = magnitude <= 5.0 * acceptable_arrival_distance # this was a TODO on the legacy code base. Legacy -> TODO 3.0 times arrival distance
        haveArrivedFinal = magnitude <= acceptable_arrival_distance and len(self.destination) == 1 
        return haveArrivedNext, haveArrivedFinal
    
    def goToNextDestination(self):
        if len(self.destination) > 1:
            self.destination.pop(0)
        return self.destination[0]
    
    def updateStatistics(self, timestep):
        self.stats.time_elapsed += timestep
        self.stats.distance_travled += timestep * self.dynamic.velocity.r
    
    def show(self):
        print(self.dynamic, ", Dest", self.destination)
        
            
        
    
    
    
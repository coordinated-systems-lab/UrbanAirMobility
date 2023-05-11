#for type hint 
from typing import List 

import cartesian2 as c2
import polar2 as p2
import aircraftstats as acs
import dynamics as dcs


class Aircraft:
    
    #constructor funciton of aircraft class, instance variables (these only belong to an instance of Aircraft object)
    def __init__(self,dynamic:dcs.Dynamics , destinations:List[c2.Cartesian2], max_acceleration:p2.Polar2, max_velocity, stats:acs.AircraftStats): #I think arrival radius is aircraft stats type obj - check please
        self.dynamic = dynamic 
        self.destination = destinations
        self.max_acceleration = max_acceleration
        self.max_velocity = max_velocity
        self.stats = stats

    #factory function 
    @classmethod
    def aircraft_(cls,dynamic:dcs.Dynamics, destinations:List[c2.Cartesian2], max_acceleration:p2.Polar2, max_velocity, arrival_radius):
        stats = acs.AircraftStats.aircraftstats_((abs(dynamic.position) - destinations[-1]),{}) - arrival_radius
        return cls(dynamic,destinations,max_acceleration,max_velocity,stats)
    
    @classmethod
    def aircraft_1(cls, dynamic:dcs.Dynamics, destinations:c2.Cartesian2, max_acceleration:p2.Polar2, max_velocity, arrival_radius):
        return cls(dynamic, [destinations], max_acceleration, max_velocity, arrival_radius)
    
    
    
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
        dcs.Dynamics.step(self.dynamic, timestep, self.max_velocity) #is it checking if velocity of aircraft is above max_velocity and if it is then setting velocity to max velocity 
        haveArrivedNext, haveArrivedFinal = self.hasArrived(acceptable_arrival_distance)
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
        self.stats.distance_traveled += timestep * self.dynamic.velocity.r
    
    def show(self):
        print(self.dynamic, ", Dest", self.destination)
        
            
        
    
    
    
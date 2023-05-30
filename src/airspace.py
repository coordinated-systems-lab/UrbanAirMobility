
import math
import numpy as np
import cartesian2 as c2
import abstractspawncontroller as abs_spwn_ctrl
import shapemanager as sm
import pathfinder as pf 
import polar2 as p2 
import airspacestats as acs
import aircraft as act
from spawnfunction import ego_spawn_function
import dynamics as dcs

from typing import List, Any
#from Shapes import ShapeManager,AbstractShape



class Airspace:
    def __init__(self, 
                 all_aircrafts: List[act.Aircraft], #not sure if numpy's ndarray would work, since this might be a mutable sequence, needs checking 
                 boundary: c2.Cartesian2, 
                 spawn_controller: abs_spwn_ctrl.AbstractSpawnController, 
                 restricted_areas: sm.ShapeManger, 
                 waypoints: pf.PathFinder, 
                 maximum_aircraft_acceleration: p2.Polar2,
                 maximum_aircraft_speed, 
                 detection_radius, 
                 arrival_radius,
                 stats: acs.AirspaceStats,
                 rng = np.random.default_rng(seed=123), 
                 create_ego_aircraft: bool = True):
        
        self.all_aircraft = all_aircrafts
        self.boundary = boundary # this attribute needs a default value (10_000,10_000)
        self.create_ego_aircraft = create_ego_aircraft #this attibute needs a default value (true)
        self.spawn_controller = spawn_controller #this attribute needs a default ConstantSpawnController(boundary, create_ego_aircraft)
        self.restricted_areas = restricted_areas #this attribute needs to be set to class ShapeManger()
        self.waypoints = waypoints #this attribute needs to be set to class PathFinder()
        
        self.maximum_aircraft_acceleration = maximum_aircraft_acceleration #this attribute needs the following :Polar2=Polar2(3.0, 2pi/10)
        self.maximum_aircraft_speed = maximum_aircraft_speed #needs value of Number 50, Number is a julia builtin Type
        self.detection_radius = detection_radius #needs default of 1000
        self.arrival_radius = arrival_radius #needs a value of 100
        
        self.stats = stats # this is belongs to the AirspaceStats class
        self.rng = rng
    
    
    
    
    @classmethod 
    def airspace(cls,
                        stats: acs.AirspaceStats,
                        all_aircrafts: List[act.Aircraft], #not sure if numpy's ndarray would work, since this might be a mutable sequence, needs checking 
                        boundary: c2.Cartesian2 = c2.Cartesian2(10000,10000), 
                        spawn_controller: abs_spwn_ctrl.AbstractSpawnController = abs_spwn_ctrl.ConstantSpawnRateController(boundary, create_ego_aircraft), #need to define ConstantSpawnRateController in abstractspawncontroller.py 
                        restricted_areas: sm.ShapeManger = sm.ShapeManger.shapemanager(), 
                        waypoints: pf.PathFinder = pf.PathFinder(), #need to provide constructor values
                        maximum_aircraft_acceleration: p2.Polar2 = p2.Polar2(3,2 * math.pi/ 10),
                        maximum_aircraft_speed = 50, 
                        detection_radius = 1000, 
                        arrival_radius = 100,
                        rng = np.random.default_rng(seed=123), 
                        create_ego_aircraft: bool = True):
        
        all_aircrafts = []
        stats = acs.AirspaceStats()


        return cls(all_aircrafts, boundary, spawn_controller, restricted_areas, waypoints, maximum_aircraft_acceleration,maximum_aircraft_speed,detection_radius,arrival_radius,stats,rng,create_ego_aircraft)
    



    def createEgoAircraft(self):
        assert len(self.all_aircraft) == 0
        #note ego is hard coded to anywhere and go 5000 meters
        start, destination = ego_spawn_function(self.boundary, c2.Cartesian2(0,0), self.detection_radius, self.arrival_radius, self.rng)
        initial_velocity = p2.Polar2(self.maximum_aircraft_speed/2, np.pi * np.random.random_sample())  
        initial_acceleration = p2.Polar2(0.0, 0.0)
        
        ac = act.Aircraft(dcs.Dynamics(start, initial_velocity, initial_acceleration), list(destination), self.maximum_aircraft_acceleration, self.maximum_aircraft_speed, self.arrival_radius)
        self.all_aircraft.append(ac) 
        
        
        
        
    def createAircraft(self, source:c2.Cartesian2, destination:c2.Cartesian2):
        destinations = pf.PathFinder.findPath(self.waypoints, source, destination, self.rng)
        
        initial_velocity = p2.Polar2(self.maximum_aircraft_speed/2, np.pi * np.random.random_sample()) #
        initial_acceleration = p2.Polar2(0.0, 0.0)

        ac = act.Aircraft(dcs.Dynamics(source,initial_velocity,initial_acceleration), destinations, self.maximum_aircraft_acceleration, self.maximum_aircraft_speed, self.arrival_radius)
        self.all_aircraft.append(ac)
        
    
    
    
    
    
    
    def findNearestIntruder(self, act.Aircraft,):
        intruder = None
        intruder_distance = self.detection_radius

        for possible_intruder in self.all_aircraft:
            if possible_intruder == aircraft:
                continue

            distance_away = Magnitude(possible_intruder.dynamic.position - aircraft.dynamic.position)
            if distance_away < intruder_distance:
                intruder = possible_intruder
                intruder_distance = distance_away
        return intruder, intruder_distance
    

    def findNearestRestricted(self, aircraft:Aircraft, restricted_areas:ShapeManager,):
        nearest_restricted, restricted_distance = getNearestPointOnEdge(restricted_areas,aircraft.dynamic.position)
        
        # make sure nearest RA is within detection radius
        if restricted_distance > self.detection_radius:
            nearest_restricted = None
            restricted_distance = self.detection_radius
        # if the AC is within the RA, then we need to adjust it.
    # The function getNearestPointOnEdge will still return an edge point, and a negative distance. 
    # we want to encourage it to leave the RA. So, we will create a point that is in the opposite direction of the nearest edge point
    # this will hopefully push the AC outside of the RA 
        if restricted_distance < 0.0:
            # get unit vector in the direction from edge to the AC
            vector_from_edge_to_ac = aircraft.dynamic.position - nearest_restricted
            unit_vector = vector_from_edge_to_ac * (1.0 / Magnitude(vector_from_edge_to_ac))
        
            #use unit vector to create a ponit on the opposite side of the ac, 50 meters away
            new_restricted_point = aircraft.dynamic.position + unit_vector * 50 
            nearest_restricted = new_restricted_point
            restricted_distance = 50
        return nearest_restricted, restricted_distance
    

    #Return the state of an aircraft 
    def getState(self, aircraft:Aircraft, restricted_areas:ShapeManager):
        #calculate deviation 
        destinantion_vector = aircraft.destinations[0] - aircraft.dynamic.position 
        deviation = Angle(destinantion_vector) - aircraft.dynamic.velocity.theta

        #find velocity 
        velocity = aircraft.dynamic.velocity.r 

        #find nearest intrider and restricted airspae.
        #Nearest point in airspace can be considered an aircraft with 0 velocity 
        #Note for both cases, if there is not an intruder/RA within detection_radius, the thing is nothing and the distance is detection_radius 
        
        nearest_intruder, intruder_distance = self.findNearestIntruder(aircraft)
        nearest_restricted, restricted_distance = self.findNearestRestricted(aircraft, restricted_areas)

        #insert comments from legacy julia codebase 
        is_intruder = intruder_distance < self.detection_radius or restricted_distance < self.detection_radius
        if intruder_distance < restricted_distance:
            intruder_distance = intruder_distance
            intruder_position = nearest_intruder.dynamic.position
            intruder_velocity = nearest_intruder.dynamic.velocity
        elif intruder_distance > restricted_distance:
            intruder_distance = restricted_distance
            intruder_position = nearest_restricted
            intruder_velocity = Polar2(0,0)

        if not(is_intruder):
            has_intruder = 0
            intruder_distance = 0
            angle_of_intruder = 0
            heading_of_intruder = 0
            velocity_of_intruder = 0

        else:
            has_intruder = 1
            angle_of_intruder = Angle(intruder_position - aircraft.dynamic.position) - aircraft.dynamic.velocity.theta
            relative_velocity_of_intruder  = toPolar(toCartesian(intruder_velocity) - toCartesian(aircraft.dynamic.velocity))
            heading_of_intruder = relative_velocity_of_intruder.theta - aircraft.dynamic.velocity.theta
            velocity_of_intruder = relative_velocity_of_intruder.r

        state = [deviation, velocity, has_intruder, intruder_distance, angle_of_intruder, heading_of_intruder, velocity_of_intruder]
        normalize_(state,aircraft.maximum_velocity,self.detection_radius)

        return state
    #insert comment from legacy julia code base 

    def normalize_(self, state, max_speed,):
        state[0] = moveBetweenPiandMinusPi(state[0])
        state[1] /= max_speed
        state[3] /= self.detection_radius
        state[4] /= moveBetweenPiandMinusPi(state[4])




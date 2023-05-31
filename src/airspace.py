
import math
import numpy as np
import cartesian2 as c2
import abstractspawncontroller as abs_spwn_ctrl
import constantspawnratecontroller as cnst_spwn_ctrlr
import shapemanager as sm
import pathfinder as pf 
import polar2 as p2 
import airspacestats as acs
import aircraft as act
from spawnfunction import ego_spawn_function
import dynamics as dcs
import convertcoordinatesystem as ccs
from typing import List, Tuple
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
                 detection_radius:float, 
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
        self.detection_radius:float = detection_radius #needs default of 1000
        self.arrival_radius = arrival_radius #needs a value of 100
        
        self.stats = stats # this is belongs to the AirspaceStats class
        self.rng = rng
    
    
    
    
    @classmethod 
    def airspace(cls,
                        stats: acs.AirspaceStats,
                        spawn_controller: cnst_spwn_ctrlr.ConstantSpawnRateController,
                        boundary: c2.Cartesian2 = c2.Cartesian2(10000,10000),  
                        restricted_areas: sm.ShapeManger = sm.ShapeManger.shapemanager(), 
                        waypoints: pf.PathFinder = pf.PathFinder.pathfinder(), # TODO this will be fixed automatically after fixing pathfinder.py 
                        maximum_aircraft_acceleration: p2.Polar2 = p2.Polar2(3,2 * math.pi/ 10),
                        maximum_aircraft_speed = 50, 
                        detection_radius = 1000, 
                        arrival_radius = 100,
                        rng = np.random.default_rng(seed=123), 
                        create_ego_aircraft: bool = True):
        
        spawn_controller = cnst_spwn_ctrlr.ConstantSpawnRateController.constantspawnratecontroller(boundary,create_ego_aircraft)
        all_aircrafts:List[act.Aircraft] = []
        stats = acs.AirspaceStats()
        
        # ? reset is defined later in the code
        # TODO - first determine what kind of method is reset, then complete the method call
        #reset()


        return cls(all_aircrafts, boundary, spawn_controller, restricted_areas, waypoints, maximum_aircraft_acceleration,maximum_aircraft_speed,detection_radius,arrival_radius,stats,rng,create_ego_aircraft)
    



    def createEgoAircraft(self):
        assert len(self.all_aircraft) == 0
        #note ego is hard coded to anywhere and goes 5000 meters
        start, destination = ego_spawn_function(self.boundary, c2.Cartesian2(0,0), self.detection_radius, self.arrival_radius, self.rng)
        initial_velocity = p2.Polar2(self.maximum_aircraft_speed/2, np.pi * np.random.random_sample())  
        initial_acceleration = p2.Polar2(0.0, 0.0)
        
        ac = act.Aircraft(dcs.Dynamics(start, initial_velocity, initial_acceleration), [destination], self.maximum_aircraft_acceleration, self.maximum_aircraft_speed, self.arrival_radius)
        self.all_aircraft.append(ac) 
        
        
        
        
    def createAircraft(self, source:c2.Cartesian2, destination:c2.Cartesian2):
        destinations = pf.PathFinder.findPath(self.waypoints, source, destination, self.rng)
        
        initial_velocity = p2.Polar2(self.maximum_aircraft_speed/2, np.pi * np.random.random_sample()) #
        initial_acceleration = p2.Polar2(0.0, 0.0)

        ac = act.Aircraft(dcs.Dynamics(source,initial_velocity,initial_acceleration), destinations, self.maximum_aircraft_acceleration, self.maximum_aircraft_speed, self.arrival_radius)
        self.all_aircraft.append(ac)
        
    
    # TODO refactor 
    def findNearestIntruder(self, aircraft:act.Aircraft) -> Tuple[act.Aircraft, float] :
        intruder : act.Aircraft 
        intruder_distance:float = self.detection_radius

        for possible_intruder in self.all_aircraft:
            if type(possible_intruder) == type(aircraft):  
                continue

            distance_away:float = abs(possible_intruder.dynamic.position - aircraft.dynamic.position)
            
            if distance_away < intruder_distance:
                intruder = possible_intruder
                intruder_distance = distance_away
        return intruder, intruder_distance
    

    def findNearestRestricted(self, aircraft:act.Aircraft,
                              restricted_areas:sm.ShapeManger,
                              detection_radius):
        
        # * restricted_area is a shape manager type object built with factory function 
        restricted_areas = restricted_areas.shapemanager() # ? defining restricted areas as factory function of shapemanager with empty list for shapes, this will cause an issue, create issue in github 
        nearest_restricted, restricted_distance = restricted_areas.getNearestPointOnEdge([],aircraft.dynamic.position)
        
        # make sure nearest RA is within detection radius
        if restricted_distance > self.detection_radius:
            nearest_restricted:c2.Cartesian2
            restricted_distance = self.detection_radius
        # if the AC is within the RA, then we need to adjust it.
    # The function getNearestPointOnEdge will still return an edge point, and a negative distance. 
    # we want to encourage it to leave the RA. So, we will create a point that is in the opposite direction of the nearest edge point
    # this will hopefully push the AC outside of the RA 
        if restricted_distance < 0.0:
            # get unit vector in the direction from edge to the AC
            vector_from_edge_to_ac = aircraft.dynamic.position - nearest_restricted
            
            # ? multiplying a cartesian with a float is unknown to Python
            # TODO need to find a way to resolve this issue
            unit_vector:c2.Cartesian2 = vector_from_edge_to_ac * (1.0 / abs(vector_from_edge_to_ac))  
        
            #use unit vector to create a point on the opposite side of the ac, 50 meters away
            new_restricted_point = aircraft.dynamic.position + unit_vector * 50 
            nearest_restricted = new_restricted_point
            restricted_distance = 50
        return nearest_restricted, restricted_distance
    
    
    #Return the state of an aircraft 
    def getState(self, 
                 aircraft:act.Aircraft,
                 all_aircraft: List[act.Aircraft],
                 detection_radius, 
                 restricted_areas:sm.ShapeManger):
        
        #calculate deviation 
        destinantion_vector = aircraft.destinations[0] - aircraft.dynamic.position 
        deviation = c2.Cartesian2.angle(destinantion_vector) - aircraft.dynamic.velocity.theta

        #find velocity 
        velocity = aircraft.dynamic.velocity.r 

        #find nearest intrider and restricted airspae.
        #Nearest point in airspace can be considered an aircraft with 0 velocity 
        #Note for both cases, if there is not an intruder/RA within detection_radius, the thing is nothing and the distance is detection_radius 
        
        nearest_intruder, intruder_distance = self.findNearestIntruder(aircraft)
        nearest_restricted, restricted_distance = self.findNearestRestricted(aircraft, restricted_areas,detection_radius)

        # * comments from legacy julia codebase 
        # first, is there an intruder or RA at all?
        # assuming there is, calculate the intruder distance away, position, and velocity
        # distance away = the ac if its closer, or the RA otherwise.
        # position = aircraft position, or the nearest point in the RA
        # velocity = ac velocity, or 0.0 for a RA


        is_intruder = intruder_distance < self.detection_radius or restricted_distance < self.detection_radius
        
        if intruder_distance < restricted_distance:
            intruder_distance = intruder_distance
            intruder_position = nearest_intruder.dynamic.position
            intruder_velocity = nearest_intruder.dynamic.velocity
        elif intruder_distance > restricted_distance:
            intruder_distance = restricted_distance
            intruder_position = nearest_restricted
            intruder_velocity = p2.Polar2(0,0)

        if not(is_intruder):
            has_intruder = 0
            intruder_distance = 0
            angle_of_intruder = 0
            heading_of_intruder = 0
            velocity_of_intruder = 0

        else:
            has_intruder = 1
            
            # ? issue with type, Pylance is unable to explicitly define the type of intruder position
            angle_of_intruder = c2.Cartesian2.angle(intruder_position - aircraft.dynamic.position) - aircraft.dynamic.velocity.theta
            
            relative_velocity_of_intruder  = ccs.toPolar(ccs.toCartesian(intruder_velocity) - ccs.toCartesian(aircraft.dynamic.velocity))
            heading_of_intruder = relative_velocity_of_intruder.theta - aircraft.dynamic.velocity.theta
            velocity_of_intruder = relative_velocity_of_intruder.r

        state = [deviation, velocity, has_intruder, intruder_distance, angle_of_intruder, heading_of_intruder, velocity_of_intruder]
        
        self.normalize(state, aircraft.max_velocity, self.detection_radius)

        return state
    #insert comment from legacy julia code base 

    @staticmethod
    def moveBetweenPiandMinusPi(angle):
        angle = angle % 2*math.pi 
        if angle < 0 :
            angle += 2* math.pi 
        if angle >= math.pi :
            angle -= 2 * math.pi 
        return angle 
    
    def normalize(self, state, max_speed, detection_radius):
        state[0] = self.moveBetweenPiandMinusPi(state[0])
        state[1] /= max_speed
        state[3] /= detection_radius
        state[4] /= self.moveBetweenPiandMinusPi(state[4]) 
        state[5] = self.moveBetweenPiandMinusPi(state[5])
        state[6] /= 2*max_speed

    def getEgoState(self):
        if self.create_ego_aircraft == False:
            raise RuntimeError('This simulation does not have an ego aircraft. set create_ego_aircraft to true in order to create an MDP') 
        return self.getState(self.all_aircraft[0], self.all_aircraft, self.detection_radius, self.restricted_areas)
    
    def getAllStates(self):
        all_states = []
        for i in range(len(self.all_aircraft)):
            if (self.create_ego_aircraft) and (i == 0) :
                continue
            ac = self.all_aircraft[i]
            all_states.append(self.getState(ac,self.all_aircraft,self.detection_radius,self.restricted_areas))
        return all_states
    
    def setEgoAcceleration(self, acceleration: p2.Polar2):
        if self.create_ego_aircraft == False:
            raise RuntimeError('This simulation does not have an ego aircraft, set ego aircraft to true in order to create an MDP')
        
        self.all_aircraft[0].setAcceleration(acceleration)
    
    # Set acceleration of every aicraft but the ego aircraft.
    # if ego exists, sets aircracts 2:N
    # if ego does not exists, sets aircrafts 1:N


    def setAllAccelerations(self, accelerations: List[p2.Polar2]):
        if (not self.create_ego_aircraft) and (len(accelerations) != len(self.all_aircraft)):
            raise RuntimeError('length of items in acceleration does not match length of all aircrafts')
        if (self.create_ego_aircraft) and (len(accelerations) != (len(self.all_aircraft) - 1)):
            raise RuntimeError('The number of acceleration values and the number of aircraft do not match. Note the ego aircraft cannot be set with this method, set it using setEgoAcceleration.')
        
        for i in range(len(accelerations)):
            if self.create_ego_aircraft:
                # TODO - might raise index out of range error since accelerations are more than aircrafts, rethink and recheck logic above
                self.all_aircraft[i+1].setAcceleration(accelerations[i])
            else:
                self.all_aircraft[i].setAcceleration(accelerations[i])
    
    
    # TODO complete step    
    def step(self, timestep, current_time, nmac_range):
        pass

    def reset(self):
        self.all_aircraft = []
        if self.create_ego_aircraft:
            self.createEgoAircraft()

    def __str__(self) -> str:
        f'num ac = {len(self.all_aircraft)}'
    
    def calculatenumNMAC(self, nmac_range, current_time):
        num_ac = len(self.all_aircraft)
        num_nmac = 0
        # * the following code comparing aircraft[0] with aircraft[1],[2],.....
        # * then i moves forward to 1 and again comparision starts between aircraft[1] with aircraft[2], [3], ......
        # * this is essentially a mapping - perform an enumeration look for tricks on youtube and other places 
        for i in range(num_ac):
            for j in i + 

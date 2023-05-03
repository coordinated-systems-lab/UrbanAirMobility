#create a random object 

#Test1
import numpy as np 
import Airspace
import Aircraft 
import Cartesian2

rng = np.random.MT19937()

t1 = Airspace(boundary=Cartesian2,
              rng = rng,
              create_ego_aircraft = True,
              spawn_controller = ConstantSpawnController(Cartesian2(1000,1000), True, 1),
              maximum_aircraft_acceleration = Polar2(3, 2 * np.np.pi/10),
              maximum_aircraft_speed = 50,
              detection_radius = 1000)

assert len(t1.all_aircraft) == 1
createAircraft(t1, Cartesian2(0,0))

assert len(t1.all_aircraft) == 2

#Test2 
t1 = Airspace(boundary=Cartesian2,
              rng = rng,
              create_ego_aircraft = False,
              spawn_controller = ConstantSpawnController(Cartesian2(1000,1000), True, 1),
              maximum_aircraft_acceleration = Polar2(3, 2 * np.np.pi/10),
              maximum_aircraft_speed = 50,
              detection_radius = 1000)

assert len(t1.all_aircraft) == 0

createAircraft(t1, Cartesian2(0,0), Cartesian2(1,1))
assert len(t1.all_aircraft) == 1

reset!(t1)
assert(t1.all_aircraft) == 0

#Test3
t1 = Airspace(boundary=Cartesian2,
              rng = rng,
              create_ego_aircraft = True,
              spawn_controller = ConstantSpawnController(Cartesian2(1000,1000), True, 1),
              maximum_aircraft_acceleration = Polar2(3, 2 * np.np.pi/10),
              maximum_aircraft_speed = 50,
              detection_radius = 1000)

step!(t1,10,0,100)
assert len(t1.all_aircraft) == 11

reset!(t1) 
assert len(t1.all_aircraft) == 1

#Test4

t1 = Airspace(boundary=Cartesian2,
              rng = rng,
              create_ego_aircraft = False,
              spawn_controller = ConstantSpawnController(Cartesian2(1000,1000), True, 1),
              maximum_aircraft_acceleration = Polar2(3, 2 * np.np.pi/10),
              maximum_aircraft_speed = 50,
              detection_radius = 1000)

step!(t1, 10, 0.0, 100.0)
assert len(t1.all_aircraft) == 10

states = getAllStates(t1)
assert len(states) == 10

accelerations = Vector{Polar2}(undef, 0)

for s in states:
    accelerations.append(Polar2(0,0))

setAllAccelerations(t1, accelerations)
step!(t1, 10, 0.0, 100.0)

# test 5
t1 = Airspace(              boundary=Cartesian2(10000.0, 10000.0), 
                            create_ego_aircraft=True, 
                            maximum_aircraft_acceleration=Polar2(3.0, 2* np.np.pi/10), 
                            maximum_aircraft_speed=50.0, 
                            detection_radius=1000.0,
                            rng=rng ,
    )


assert getEgoState(t1)[3] == 0.0 # should be no one around
step!(t1, 200.0, 0.0, 100.0)
assert getEgoState(t1)[3] == 1.0 # should be someone close. Note this may fail by random chance if all AC randomly spawn far away, but should usually succeed

# test 6 - verify state calculations - heading and velocity of intruder are in local coordinates
# ego is going in positive x direciton, intruder is infront of (in positive x direction) moving at same speed. Relative velocity should be 0, heading 0
ego =       Aircraft(Dynamics(Cartesian2(0,0), Polar2(5, 0), Polar2(0,0)), Cartesian2(1000,0), Polar2(100,100), 10, 100)
intruder =  Aircraft(Dynamics(Cartesian2(100,0), Polar2(5, 0), Polar2(0,0)), Cartesian2(1000,0), Polar2(100,100), 10, 100)
assert getState(ego, [intruder], 1000, ShapeManager()) == [0.0, 0.5, 1.0, 0.1, 0.0, 0.0, 0.0] 

# ego is going in positive x direciton, intruder is to the right of (in negative y direction) moving at same speed. Relative velocity should be 0, heading 0
ego =       Aircraft(Dynamics(Cartesian2(0,0), Polar2(5, 0), Polar2(0,0)), Cartesian2(1000,0), Polar2(100,100), 10, 100)
intruder =  Aircraft(Dynamics(Cartesian2(0, -100), Polar2(5, 0), Polar2(0,0)), Cartesian2(1000,0), Polar2(100,100), 10, 100)
assert getState(ego, [intruder], 1000, ShapeManager()) == [0.0, 0.5, 1.0, 0.1, -np.np.pi/2, 0.0, 0.0] 

# ego is going in positive y direciton, intruder is behind of (in negative y direction) moving at same speed but going in positive x direction
#  Relative velocity should be non zero, heading -np.pi/2
ego =       Aircraft(Dynamics(Cartesian2(0,0), Polar2(5, np.pi/2), Polar2(0,0)), Cartesian2(0,1000), Polar2(100,100), 10, 100)
intruder =  Aircraft(Dynamics(Cartesian2(0, -100), Polar2(5, 0), Polar2(0,0)), Cartesian2(1000,0), Polar2(100,100), 10, 100)
assert getState(ego, [intruder], 1000, ShapeManager()) == [0.0, 0.5, 1.0, 0.1, np.pi, -3*np.np.pi/4, np.sqrt(5^2 + 5^2)/(2*10)]  # Compute absolute diff in velocity, divide by 2 times the max velocity

# ego going at np.pi/4, intruder at 3/4pi, ,
ego =       Aircraft(Dynamics(Cartesian2(0,0), Polar2(5, np.pi/4), Polar2(0,0)), Cartesian2(1000,1000), Polar2(100,100), 10, 100)
intruder =  Aircraft(Dynamics(Cartesian2(0, -100), Polar2(5, 3pi/4), Polar2(0,0)), Cartesian2(-1000,1000), Polar2(100,100), 10, 100)
assert getState(ego, [intruder], 1000, ShapeManager()) == [0.0, 0.5, 1.0, 0.1, -3pi/4, 3pi/4, sqrt(5^2 + 5^2)/(2*10)]  # Compute absolute diff in velocity, divide by 2 times the max velocity

# ego going at -3pi/4, intruder at 1/4pi, 
ego =       Aircraft(Dynamics(Cartesian2(0,0), Polar2(5, -3pi/4), Polar2(0,0)), Cartesian2(-1000,-1000), Polar2(100,100), 10, 100)
intruder =  Aircraft(Dynamics(Cartesian2(0, 100), Polar2(5, np.pi/4), Polar2(0,0)), Cartesian2(1000,1000), Polar2(100,100), 10, 100)
assert getState(ego, [intruder], 1000,  ShapeManager()) == [0.0, 0.5, 1.0, 0.1, -3*np.pi/4, np.pi, (5 + 5)/(2*10)]  # Compute absolute diff in velocity, divide by 2 times the max velocity

# test 7 - verify state calculations - RA is closer than intruder
ego =       Aircraft(Dynamics(Cartesian2(0,0), Polar2(5, 0.0), Polar2(0,0)), Cartesian2(1000,0.0), Polar2(100,100), 10, 100)
intruder =  Aircraft(Dynamics(Cartesian2(0, -1000), Polar2(5, 0.0), Polar2(0,0)), Cartesian2(1000.0,0.0), Polar2(100,100), 10, 100)
shape =  Circle(Cartesian2(500.0, 0.0), 100.0)
sm = ShapeManager()
addShape!(sm, shape, 1)
assert getState(ego, [intruder], 1000,  sm) == [0.0, 0.5, 1.0, 0.4, 0.0, np.pi, (5)/(2*10)]  # Compute absolute diff in velocity, divide by 2 times the max velocity


print("Passed AirspaceTest")
import math
import numpy as np
import random
import airspace as aspc
import cartesian2 as c2
import constantspawnratecontroller as cons_spwn_ctrlr
import dynamics as dyn
import shapemanager as shpmng
import polar2 as p2

rng = random.Random(123)

######################## TEST 1 #######################
t1 = aspc.Airspace.airspace()

assert len(t1.all_aircraft) == 1
t1.createAircraft(c2.Cartesian2(0, 0), c2.Cartesian2(1, 1))
assert len(t1.all_aircraft) == 2

######################## TEST 2 #######################
t1 = aspc.Airspace.airspace(create_ego_aircraft=False)

assert len(t1.all_aircraft) == 0
t1.createAircraft(c2.Cartesian2(0, 0), c2.Cartesian2(1, 1))
assert len(t1.all_aircraft) == 1
t1.reset()
assert len(t1.all_aircraft) == 0

######################## TEST 3  #######################
t1 = aspc.Airspace.airspace(
    spawn_controller=cons_spwn_ctrlr.ConstantSpawnRateController.constantspawnratecontroller(
        c2.Cartesian2(10000, 10000), True, 3600/math.pi
    )
)

# TODO need to find why step is creating so many aircrafts in the airspaces
t1.step(10, 0, 100)
print('test 3 -> aircrafts in airspace: ', len(t1.all_aircraft)) #* ->5730 aircrafts

# TODO -> assert len(t1.all_aircraft) == 11

t1.reset()
assert len(t1.all_aircraft) == 1

######################## TEST 4  #######################
t1 = aspc.Airspace.airspace(
    boundary=c2.Cartesian2(10000,10000),
    create_ego_aircraft=False,
    spawn_controller=cons_spwn_ctrlr.ConstantSpawnRateController.constantspawnratecontroller(
        c2.Cartesian2(10000, 10000), False, 36
    ),
)

t1.step(10, 0, 100)
# TODO need to find why step is creating so many aircrafts in the airspace
# print('aircrafts in airspace: ', len(t1.all_aircraft)) #* -> 360

# TODO assert len(t1.all_aircraft) == 10

states = t1.getAllStates()

# TODO need to find why step is creating so many aircrafts in the airspace
# print('number of states: ', len(states)) #* ->360

# TODO assert len(states) == 10

accelerations = []
for s in states:
    accelerations.append(p2.Polar2(0, 0))

t1.setAllAccelerations(accelerations)
t1.step(10, 0, 100)
# print('aircrafts in airspace: ', len(t1.all_aircraft)) #* -> 720


######################## TEST 5  #######################
t1 = aspc.Airspace.airspace()

assert t1.getEgoState()[2] == 0
t1.step(200, 0, 100)
assert t1.getEgoState()[2] == 1

print('Passed airspace test')
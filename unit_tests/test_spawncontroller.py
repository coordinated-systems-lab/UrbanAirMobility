# Test constant spawn controller 
# create variables 
import random
import math
import aircraft as acft
import dynamics as dcs
import shapemanager as shpmng 
import rectangle as rtngl
import circle
import polar2 as p2
import cartesian2 as c2
import constantspawnratecontroller as cnstspwnctrl
import queuedspawncontroller

sources = shpmng.ShapeManger.shapemanager()
dests = shpmng.ShapeManger.shapemanager()

sources.addShape(rtngl.Rectangle.rectangle(c2.Cartesian2(0,1000), c2.Cartesian2(1000,0),True))
dests.addShape(rtngl.Rectangle.rectangle(c2.Cartesian2(0,1000), c2.Cartesian2(1000,0),True))

sc = cnstspwnctrl.ConstantSpawnRateController.constantspawnratecontroller_1(sources = sources, destinations= dests, spawns_per_km_squared_hours=3600, relative_destination=True )

#must return 1 ax based on the spawnrate, 3600 per km^2 and a timestep of 1 second

list_ = sc.getSourceandDestinations(1, 0, [], c2.Cartesian2(0,0))
assert len(list_) == 1 

list_ = sc.getSourceandDestinations(1, 0, [], c2.Cartesian2(0,0))
assert len(list_) == 1 

list_ = sc.getSourceandDestinations(1, 0, [], c2.Cartesian2(0,0))
assert len(list_) == 1 

#doubling shoule be 2 now
sc.setSpawnRate(7200)

list_ = sc.getSourceandDestinations(1, 0, [], c2.Cartesian2(0,0))
assert len(list_) == 2

list_ = sc.getSourceandDestinations(1, 0, [], c2.Cartesian2(0,0))
assert len(list_) == 2

# Testing queuedspawncontroller 

qsc = queuedspawncontroller.QueuedSpawnController.queuedspawncontroller(sources=sources, destinations=dests, spawns_per_km_squared_hours=3600, relative_destination=False)

# no ac, should be able to spawn 1
list_ = qsc.getSourceAndDestinations(1, 0, [], c2.Cartesian2(0,0))
assert len(list_) == 1

#can only spawn 1 at a time since then they are too close anyway, so even if spawnrate is high
#still only return 1 
qsc.setSpawnRate(36000)
list_ = list_ = qsc.getSourceAndDestinations(1, 0, [], c2.Cartesian2(0,0))
assert len(list_) == 1

#now testing congested airspace 

sources = shpmng.ShapeManger.shapemanager()
dests = shpmng.ShapeManger.shapemanager()
sources.addShape(circle.Circle.circle(c2.Cartesian2(1000.0, 1000.0), 500.0,r_dist=random.uniform(0,10),angle_dist=random.uniform(0,2*math.pi),clip=True))
dests.addShape(circle.Circle.circle(c2.Cartesian2(1000,1000),500, r_dist=random.uniform(0,10),angle_dist=random.uniform(0,2*math.pi),clip=True))

ac = []
ac.append(acft.Aircraft.aircraft_1(dcs.Dynamics(c2.Cartesian2(1000,1000),p2.Polar2(0,0),p2.Polar2(0,0)),c2.Cartesian2(10000,10000),p2.Polar2(0,0),1000,1))
qsc = queuedspawncontroller.QueuedSpawnController.queuedspawncontroller(sources=sources, destinations=dests, spawns_per_km_squared_hours=3600/(math.pi/4),relative_destination=False)

# note we have 3600*pi/4 spawns/km2hr, pi/4 area, 1 second sim, should get 1 ac.
# but we have forced it to spawn at exactly 1000,1000
# and we added an ac at 1000, 1000
# so it should stay in queue and NOT spawn

list_ = qsc.getSourceAndDestinations(1,0,ac,c2.Cartesian2(0,0))
assert len(list_) == 0

#now if aircraft is empty, can spawn again
list_ = qsc.getSourceAndDestinations(1,0,[],c2.Cartesian2(0,0))
assert len(list_) == 1

# double spawn rate will still spawn 1, due to spacing issue
qsc.setSpawnRate(2*(3600/(4*math.pi)))
list_ = qsc.getSourceAndDestinations(1,0,[],c2.Cartesian2(0,0))
assert len(list_) == 1

print('Passed SpawnController testing')



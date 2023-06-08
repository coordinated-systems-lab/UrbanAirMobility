
import aircraft as acft, dynamics as dcs, cartesian2 as c2, polar2 as p2
import math

error = 0.001

# Test 1 
#                   dynamic :    position,          velocity,      acceleration
t1 = acft.Aircraft(dcs.Dynamics(c2.Cartesian2(0,0),p2.Polar2(0,0),p2.Polar2(5,math.pi)), #why did Julia code have 0,0
                   [c2.Cartesian2(10,0)],
                   p2.Polar2(5,math.pi),
                   10,
                   100)


t1.setAcceleration(p2.Polar2(10_000, 2*math.pi))

assert t1.dynamic.acceleration.r == 5   
assert t1.dynamic.acceleration.theta == math.pi

# Test 2 
t1 = acft.Aircraft(dcs.Dynamics(c2.Cartesian2(0,0),p2.Polar2(0,0),p2.Polar2(0,0)),
                   [c2.Cartesian2(10,0)],
                   p2.Polar2(5,math.pi),
                   10,
                   100)



assert t1.hasArrived(100) == (True, True)
assert t1.hasArrived(1) == (False, False)


# Test 3
t1 = acft.Aircraft(dcs.Dynamics(c2.Cartesian2(0,0),p2.Polar2(0,0),p2.Polar2(0,0)),
                   [c2.Cartesian2(10,0), c2.Cartesian2(1000,0)],
                   p2.Polar2(5,math.pi),
                   10,
                   100)

assert t1.hasArrived(100) == (True, False)

print('All aircraft test complete')
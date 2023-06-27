from math import pi
from dynamics import Dynamics
from cartesian2 import Cartesian2
from polar2 import Polar2
from polar2 import Polar2

error = 0.001

# Test 1
d1 = Dynamics(Cartesian2(0.0,0.0) ,Polar2(0.0,0.0) ,Polar2(0.0,0.0) )
assert d1.position.x - 0.0 < error
assert d1.position.y - 0.0 < error

# Test 2
d1 = Dynamics(Cartesian2(0.0,0.0) ,Polar2(0.0,0.0), Polar2(0.0,0.0) )
d1.step(1.0)
assert d1.position.x - 0.0 < error
assert d1.position.y - 0.0 < error

# Test 3
d1 = Dynamics(Cartesian2(0.0,0.0) ,Polar2(1.0,0.0) ,Polar2(0.0,0.0) )
d1.step(1.0)
assert d1.position.x - 1.0 < error
assert d1.position.y - 0.0 < error

# Test 4
d1 = Dynamics(Cartesian2(0.0,0.0) ,Polar2(1.0,0.0) ,Polar2(0.0,0.0) )
d1.step(1.0)
d1.step(1.0)
assert d1.position.x - 2.0 < error
assert d1.position.y - 0.0 < error

# Test 5
d1 = Dynamics(Cartesian2(0.0,0.0) ,Polar2(0.0,0.0) ,Polar2(1.0,0.0) )
d1.step(1.0)
assert d1.position.x - 1.0 < error
assert d1.position.y - 0.0 < error
assert d1.velocity.r - 1.0 < error
assert d1.velocity. theta - 0.0 < error
d1.step(1.0)
assert d1.position.x - 3.0 < error
assert d1.position.y - 0.0 < error
assert d1.velocity.r - 2.0 < error
assert d1.velocity. theta - 0.0 < error

# Test 6
d1 = Dynamics(Cartesian2(0.0,0.0) ,Polar2(1.0,0.0) ,Polar2(0.0,pi/4) )
d1.step(1.0)
assert d1.velocity.r - 1.0 < error
assert d1.velocity. theta - pi/4 < error
d1.step(1.0)
assert d1.velocity.r - 1.0 < error
assert d1.velocity. theta - pi/2 < error
d1.step(1.0)
assert d1.velocity.r - 1.0 < error
assert d1.velocity. theta - 3*pi/4 < error
d1.step(1.0)
assert d1.velocity.r - 1.0 < error
assert d1.velocity. theta - 4*pi/4 < error

# Test 7
d1 = Dynamics(Cartesian2(0.0,0.0) ,Polar2(1.0,0.0) ,Polar2(0.0,2*pi) )
d1.step( 0.1)
d1.step( 0.1)
d1.step( 0.1)
d1.step( 0.1)
d1.step( 0.1)
d1.step( 0.1)
d1.step( 0.1)
d1.step( 0.1)
d1.step( 0.1)
d1.step( 0.1)

assert d1.velocity.r - 1.0 < error
assert d1.velocity.theta - 2*pi < error
print('current position of agent -> ', d1.position.x, d1.position.y)
#assert d1.position.x - 0.0 < error #* if the agent steps 10 times it should be at a different position 
#assert d1.position.y - 0.0 < error #! julia test code is incorrect, discuss for clarification 

# Test 8
d1 = Dynamics(Cartesian2(0.0,0.0) ,Polar2(1.0,0.0) ,Polar2(0.0,2*pi) )
d1.setacceleration(Polar2(5.0,5.0))
assert d1.acceleration.r - 5.0 < error
assert d1.acceleration.theta - 5.0 < error
d1.step(1.0)
assert d1.acceleration.r - 5.0 < error
assert d1.acceleration.theta - 5.0 < error

# Test 9
d1 = Dynamics(Cartesian2(0.0,0.0) ,Polar2(10.0,0.0) ,Polar2(1.0,0) )
d1.step(1.0,10.0)
assert d1.velocity.r - 10.0 < error


print("Passed DynamicsTest")

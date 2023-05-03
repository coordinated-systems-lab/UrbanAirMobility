import numpy as np
error = 0.001

# Test 1
d1 = Dynamics(Cartesian2(0.0,0.0), Polar2(0.0,0.0), Polar2(0.0,0.0) )
assert d1.position.x - 0.0 < error
assert d1.position.y - 0.0 < error

# Test 2
d1 = Dynamics(Cartesian2(0.0,0.0), Polar2(0.0,0.0), Polar2(0.0,0.0) )
step!(d1, 1.0)
assert d1.position.x - 0.0 < error
assert d1.position.y - 0.0 < error

# Test 3
d1 = Dynamics(Cartesian2(0.0,0.0), Polar2(1.0,0.0), Polar2(0.0,0.0) )
step!(d1, 1.0)
assert d1.position.x - 1.0 < error
assert d1.position.y - 0.0 < error

# Test 4
d1 = Dynamics(Cartesian2(0.0,0.0), Polar2(1.0,0.0), Polar2(0.0,0.0) )
step!(d1, 1.0)
step!(d1, 1.0)
assert d1.position.x - 2.0 < error
assert d1.position.y - 0.0 < error

# Test 5
d1 = Dynamics(Cartesian2(0.0,0.0), Polar2(0.0,0.0), Polar2(1.0,0.0) )
step!(d1, 1.0)
assert d1.position.x - 1.0 < error
assert d1.position.y - 0.0 < error
assert d1.velocity.r - 1.0 < error
assert d1.velocity.θ - 0.0 < error
step!(d1, 1.0)
assert d1.position.x - 3.0 < error
assert d1.position.y - 0.0 < error
assert d1.velocity.r - 2.0 < error
assert d1.velocity.θ - 0.0 < error

# Test 6
d1 = Dynamics(Cartesian2(0.0,0.0), Polar2(1.0,0.0), Polar2(0.0,np.pi/4) )
step!(d1, 1.0)
assert d1.velocity.r - 1.0 < error
assert d1.velocity.θ - np.pi/4 < error
step!(d1, 1.0)
assert d1.velocity.r - 1.0 < error
assert d1.velocity.θ - np.pi/2 < error
step!(d1, 1.0)
assert d1.velocity.r - 1.0 < error
assert d1.velocity.θ - 3*np.pi/4 < error
step!(d1, 1.0)
assert d1.velocity.r - 1.0 < error
assert d1.velocity.θ - 4*np.pi/4 < error

# Test 7
d1 = Dynamics(Cartesian2(0.0,0.0), Polar2(1.0,0.0), Polar2(0.0,2pi) )
step!(d1, 0.1)
step!(d1, 0.1)
step!(d1, 0.1)
step!(d1, 0.1)
step!(d1, 0.1)
step!(d1, 0.1)
step!(d1, 0.1)
step!(d1, 0.1)
step!(d1, 0.1)
step!(d1, 0.1)

assert d1.velocity.r - 1.0 < error
assert d1.velocity.θ - 2*np.pi < error
assert d1.position.x - 0.0 < error
assert d1.position.y - 0.0 < error

# Test 8
d1 = Dynamics(Cartesian2(0.0,0.0), Polar2(1.0,0.0), Polar2(0.0,2pi) )
setAcceleration!(d1, Polar2(5.0, 5.0))
assert d1.acceleration.r - 5.0 < error
assert d1.acceleration.θ - 5.0 < error
step!(d1, 1.0)
assert d1.acceleration.r - 5.0 < error
assert d1.acceleration.θ - 5.0 < error

# Test 9
d1 = Dynamics(Cartesian2(0.0,0.0), Polar2(10.0,0.0), Polar2(1.0,0) )
step!(d1, 1.0, 10.0)
assert d1.velocity.r - 10.0 < error


print("Passed DynamicsTest")
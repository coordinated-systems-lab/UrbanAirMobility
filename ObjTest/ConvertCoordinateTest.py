import numpy as np
error = 0.00001

# Test 1
t1 = toPolar(Cartesian2(5,0))
assert t1.r - 5.0 < error
assert t1.θ - 0.0 < error

# Test 2
t1 = toPolar(Cartesian2(0,5))
assert t1.r - 5.0 < error
assert t1.θ - np.pi/2 < error

# Test 3
t1 = toPolar(Cartesian2(-5,0))
assert t1.r - 5.0 < error
assert t1.θ - np.pi < error

# Test 4
t1 = toPolar(Cartesian2(0,-5))
assert t1.r - 5.0 < error
assert t1.θ - -np.pi/2 < error

# Test 5
t1 = toCartesian(Polar2(5,0))
assert t1.x - 5.0 < error
assert t1.y - 0.0 < error

# Test 6
t1 = toCartesian(Polar2(5,np.pi/2))
assert t1.x - 0.0 < error
assert t1.y - 5.0 < error

# Test 7
t1 = toCartesian(Polar2(5,np.pi))
assert t1.x - -5.0 < error
assert t1.y - 0.0 < error

# Test 8
t1 = toCartesian(Polar2(5,3pi/2))
assert t1.x - 0.0 < error
assert t1.y - -5.0 < error

# Test 9
t1 = toCartesian(Polar2(5,2pi))
assert t1.x - 5.0 < error
assert t1.y - 0.0 < error

print("Passed ConvertCoordinateSystemTest")
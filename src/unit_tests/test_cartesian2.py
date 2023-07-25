from math import pi as pi 
from modules.cartesian2 import Cartesian2 as Cartesian2

error = 0.00001

# Test 1
t1 = Cartesian2(0,0) + Cartesian2(1,1)
assert t1.x == 1
assert t1.y == 1

# Test 2
t1 = Cartesian2(0,0) - Cartesian2(1,1)
assert t1.x == -1
assert t1.y == -1

# Test 3
t1 = Cartesian2(0.0,0.0) + Cartesian2(1.0,1.0)
assert t1.x == 1.0
assert t1.y == 1.0

# Test 4
t1 = Cartesian2(0.0,0.0) - Cartesian2(1.0,1.0)
assert t1.x == -1.0
assert t1.y == -1.0

# Test 5
t1 = Cartesian2(4.0,3.0)
assert abs(t1) == 5.0

# Test 6
t1 = Cartesian2(4.0,4.0)
assert t1.angle() - pi/4 < error

# Test 7
t1 = Cartesian2(-4.0,4.0)
assert t1.angle() - 3*pi/4 < error

# Test 8
t1 = Cartesian2(-4.0,-4.0)
assert t1.angle() - -3*pi/4 < error

# Test 9
t1 = Cartesian2(4.0,-4.0)
assert t1.angle() - -pi/4 < error

# Test 10
t1 = Cartesian2(1.0, 1.0) * 10
assert t1.x == 10.0
assert t1.y == 10.0

# Test 11
t1 = Cartesian2(1.0, 1.0) * 0.1
assert t1.x == 0.1
assert t1.y == 0.1

# Test 12
t1 = Cartesian2(1.0, 1.0) * -0.1
assert t1.x == -0.1
assert t1.y == -0.1

# Test 13
t1 = Cartesian2(1.0, 1.0)
t2 = Cartesian2(1.0, 1.0)
assert t1 == t2

print("Passed Cartesian2Test")
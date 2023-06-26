from polar2 import Polar2 as P
from math import pi as pi 

error = 0.001 

#Test1 
t1 = P(0,0) + P(1,1)

assert t1.r == 1
assert t1.theta == 1

#Test 2 
t1 = P(0,0) - P(1,1)

assert t1.r == -1
assert t1.theta == -1

#Test 3
t1 = P(1,1) * 10 #! scalars can only be multiplied in this form 

assert t1.r == 10
assert t1.theta == 10

# Test 4
t1 = P(0.0,0.0)

assert t1.getX() - 0.0 < error
assert t1.getY() - 0.0 < error

# Test 5
t1 = P(5.0,0.0)
assert t1.getX() - 5.0 < error
assert t1.getY() - 0.0 < error

# Test 6
t1 = P(5.0,pi/2)
assert t1.getX() - 0.0 < error
assert t1.getY() - 5.0 < error

# Test 7
t1 = P(5.0,pi)
assert t1.getX() - -5.0 < error
assert t1.getY() - 0.0 < error

# Test 8
t1 = P(5.0,3*pi/2)
assert t1.getX() - 0.0 < error
assert t1.getY() - -5.0 < error

# Test 9
t1 = P(5.0,2*pi)
assert t1.getX() - 5.0 < error
assert t1.getY() - 0.0 < error

# Test 10
t1 = P(5.0,20*pi)
assert t1.getX() - 5.0 < error
assert t1.getY() - 0.0 < error

# Test 10
t1 = P(5.0,pi/4)
assert t1.getX() - 3.53553 < error
assert t1.getY() - 3.53553 < error
print("Passed polar2 test")
from math import pi 
from modules import pilotfunction as pf
from modules.polar2 import Polar2


# test 1
pilot = pf.default_pilot_function(Polar2(5.0, pi))

# test 2
state1 = [2, 5.0,0,0,0,0,0]
assert pilot(state1)[1] > 0.0
assert pilot(state1)[0] == 0.0

# test 3
state1 = [-2,5.0,0,0,0,0,0]
assert pilot(state1)[1] < 0.0
assert pilot(state1)[0] == 0.0

print("Passed PilotFunctionTest")
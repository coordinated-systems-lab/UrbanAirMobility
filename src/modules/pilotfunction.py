# Dependencies: Cartesian2, Polar2, ConvertCoordinateSystem, Dynamics, Aircraft, Airspace

# Here is the interface for a custom pilot function
# your function must take 1 argument: The state array
# Additionally, provides a RNG. You must use this to generate randomness (if you choose to), or your results will not be reproducible. 

# your function must return 1 action array
# To see what the state and action array consists of, see the MDP

# The below function is a default pilot behavior. It goes straight to the destination, ignoring intruders.
# Slight noise is added to make the aircraft swerve
import random
from modules import polar2 as p2

def default_pilot_function(max_acceleration:p2.Polar2) :
    def some_pilot_function(state,rng = random.Random(123)): # here 'rng' will need to call numpy to return a random number generator
        max_turn_rate = max_acceleration.theta
        deviation = state[0]
        
        # * python does not have a default clamp function, below we have python code that accomplishes the same 
        if (deviation >= -max_turn_rate) and (deviation <= max_turn_rate):
            turn_direction = deviation 
        elif deviation < -max_turn_rate:
            turn_direction = -max_turn_rate
        elif deviation > max_turn_rate:
            turn_direction = max_turn_rate
        
        action = [0, turn_direction] #type: ignore
        return action
    return some_pilot_function

        
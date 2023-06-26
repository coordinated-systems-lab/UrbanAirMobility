# the below function creates the ego agents initial position and destination for the MDP. The destination is guranteed to be exactly 5000 meters away. 

# this script makes a call to numpy,
# should we call numpy everytime we use a method from it 
# or should we have a dependencies file that contains all the dependencies 
#and from there have the file as a header for all other files 
#that way we can use any package as needed

import numpy as np
from cartesian2 import Cartesian2 as c2
from polar2 import Polar2 as p2
import convertcoordinatesystem as ccs

def ego_spawn_function(boundary:c2, ego_location:c2, detection_radius, arrival_radius, rng = np.random.default_rng(123)): #why is this function using so many inputs when only one is being used
    init_x = rng.uniform(0,boundary.x) # need to check the data type, here init_x is float, julia outputs it to type rng
    init_y = rng.uniform(0,boundary.y) # same as before, chk data type of 'rng'
    
    dest_theta = (2*np.pi) * np.random.random_sample()
    dest_offset = ccs.toCartesian(p2(5000,dest_theta))
    
    start = c2(init_x, init_y)
    destination = start + dest_offset
    
    return start, destination

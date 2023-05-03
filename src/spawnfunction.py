# the below function creates the ego agents initial position and destination for the MDP. The destination is guranteed to be exactly 5000 meters away. 

# this script makes a call to numpy,
# should we call numpy everytime we use a method from it 
# or should we have a dependencies file that contains all the dependencies 
#and from there have the file as a header for all other files 
#that way we can use any package as needed

import numpy as np

def ego_spawn_function(boundary:Cartesian2, ego_location:Cartesian2, detection_radius, arrival_radius, rng):
    init_x = np.random.uniform(0,boundary.x) # need to check the data type, here init_x is float, julia outputs it to type rng
    init_y = np.random.uniform(0,boundary.y) # same as before, chk data type of 'rng'
    
    dest_theta = np.random.uniform(0,2*np.pi)
    dest_offset = toCartesian(Polar2(5000,dest_theta))
    
    start = Cartesian2(init_x, init_y)
    destination = start + dest_offset
    
    return start, destination

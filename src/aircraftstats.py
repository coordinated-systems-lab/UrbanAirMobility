
import uuid

class AircraftStats():
    def __init__(self, ideal_distance, ac_encountered:dict, unique_id = uuid.uuid1(),distance_traveled=0, time_elapsed=0, num_nmac=0): #check if uuid1() is a predefined Julia function or defined function in AAM project or not
        self.ideal_distance = ideal_distance
        self.distance_traveled = distance_traveled
        self.time_elapsed = time_elapsed
        self.num_nmac = num_nmac
        self.unique_id = unique_id
        self.ac_encountered = ac_encountered

#need to check and understand if these functions are class methods or are they regular functions 
#also need to learn can these functions be used in some other script where AircraftStats class are being used
#how can I use functions defined in this script in other scripts - possible answer -> header files check python header files
def getNormalizedRouteLength(acs:AircraftStats):
    return acs.distance_traveled / acs.ideal_distance
    
def getAverageVelocity(acs:AircraftStats):
    return acs.distance_traveled/acs.time_elapsed
    
def getNMACPerSecond(acs:AircraftStats):
    return acs.num_nmac / acs.time_elapsed
    
    
    
    
        
    
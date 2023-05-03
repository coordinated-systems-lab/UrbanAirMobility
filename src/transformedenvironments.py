# Dependencies: Cartesian2, Polar2, ConvertCoordinateSystem, Dynamics, Aircraft, SpawnFunction, PilotFunction, Airspace, MDP


# this function returns an environment that does not allow linear acceleration, only a change in direction
# it is a simpler problem to solve

######## ^^^ #########
######## ||| ######### 
#above comments are from legacy code 


def getDirectionOnlyEnvironment(env:CollisionAvoidanceEnv):
    
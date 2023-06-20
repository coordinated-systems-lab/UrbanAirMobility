# dependencies: none
import random
# converts a spawnrate measured in flights per km^2 hours to flights per m^2 seconds
rng = random.random()

def km_sq_hrs_to_m_sq_secs(spawnrate):
    return spawnrate * (1/1000)**2 * (1/3600)

def makeInt(x, rng = rng):
    ret = int(x)

    decimal = x - ret

    if rng < decimal:
        ret += 1
    
    return ret
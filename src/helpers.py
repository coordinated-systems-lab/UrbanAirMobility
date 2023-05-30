# dependencies: none

# converts a spawnrate measured in flights per km^2 hours to flights per m^2 seconds
def km_sq_hrs_to_m_sq_secs(spawnrate):
    return spawnrate * (1/1000)**2 * (1/3600)


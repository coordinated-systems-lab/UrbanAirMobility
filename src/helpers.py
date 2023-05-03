# dependencies: none

# converts a spawnrate measured in flights per km^2 hours to flights per m^2 seconds
function KMSquaredHoursstoMSquaredSeconds(spawnrate)
    return spawnrate * (1.0/1000.0)^2.0 * (1.0/3600.0)
end


# turns the float into an int. Probability of being the floor or ceiling is proportional to the decimal of the float
function makeInt(x, rng)
    ret = trunc(x)
    
    # random chance to adjust based on decimal size
    decimal = x-ret
    if rand(rng, Uniform(0.0, 1.0)) < decimal
        ret += 1
    end

    return ret
end
# Dependencies: Cartesian2, Polar2, ConvertCoordinateSystem, Dynamics, Aircraft


mutable struct ConstantSpawnrateController <: AbstractSpawnController
    sources::ShapeManager
    destinations::ShapeManager
    spawnrate_per_second::Number
    relative_destination::Bool
end

function ConstantSpawnrateController(boundary::Cartesian2, is_mdp::Bool, spawns_per_kilometer_squared_hours =50.0)
    # default spawn locations and destination is uniform within the boundary. Note this is for non-ego agents only
    # ego agent gets a random spawn and destination always!

    sources = ShapeManager()
    destinations = ShapeManager()

    if is_mdp
        addShape!(sources,      Circle(Cartesian2(0.0, 0.0), 1000.0, r_distribution=Uniform(150.0, 1000.0)), 1) # for mdp, default to circle. Will be adjusted to be around ego
        addShape!(destinations, Circle(Cartesian2(0.0, 0.0), 2000.0, r_distribution=Uniform(150.0, 2000.0)), 1) # for mdp, default to circle. Will be adjusted to be around ego
    else
        addShape!(sources,      Rectangle(Cartesian2(0.0, boundary.y), Cartesian2(boundary.x, 0.0)), 1) # for sim, default to uniform square
        addShape!(destinations, Rectangle(Cartesian2(0.0, boundary.y), Cartesian2(boundary.x, 0.0)), 1) # for sim, default to uniform square
    end
    return ConstantSpawnrateController(sources=sources, destinations=destinations, spawns_per_km_squared_hours=spawns_per_kilometer_squared_hours, relative_destination=is_mdp)
end

function ConstantSpawnrateController(;  sources::ShapeManager,
                                        destinations::ShapeManager,
                                        spawns_per_km_squared_hours::Number,
                                        relative_destination::Bool)
    spawns_per_meter_squared_seconds = KMSquaredHoursstoMSquaredSeconds(spawns_per_km_squared_hours)
    spawns_per_seconds = spawns_per_meter_squared_seconds * getArea(sources)
    return ConstantSpawnrateController(sources, destinations, spawns_per_seconds, relative_destination)
end


# must return a vector of Tuple of cartesian 2 points
function getSourceAndDestinations(sc::ConstantSpawnrateController, timestep::Number, current_time::Number, aircraft::Vector{Aircraft}, ego_position::Cartesian2, rng::AbstractRNG)
    ac_to_spawn = makeInt(sc.spawnrate_per_second * timestep, rng)
    
    ret = Vector{Tuple{Cartesian2, Cartesian2}}(undef, 0)
    for i in 1:ac_to_spawn
        start = samplePoint(sc.sources, rng) + ego_position
        destination = samplePoint(sc.destinations, rng)
        if sc.relative_destination
            destination += start
        end
        push!(ret, (start, destination))
    end
    
    return ret
end

function setSpawnRate(sc::ConstantSpawnrateController, spawns_per_km_squared_hours::Number)
    spawns_per_meter_squared_seconds = KMSquaredHoursstoMSquaredSeconds(spawns_per_km_squared_hours)
    spawns_per_seconds = spawns_per_meter_squared_seconds * getArea(sc.sources)
    sc.spawnrate_per_second = spawns_per_seconds
end

function render(sc::ConstantSpawnrateController, ax)
	render(sc.sources, ax, "g", ":") # dotted line
	render(sc.destinations, ax, "b", ":") # dotted line
end
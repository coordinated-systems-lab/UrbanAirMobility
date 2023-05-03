# Dependencies: Cartesian2, Polar2, ConvertCoordinateSystem, Dynamics, Aircraft


mutable struct QueuedSpawnController <: AbstractSpawnController
    sources::ShapeManager
    destinations::ShapeManager
    queues::Vector{Int}
    spawnrate_per_second::Number
    relative_destination::Bool
end


function QueuedSpawnController(;        sources::ShapeManager,
                                        destinations::ShapeManager,
                                        spawns_per_km_squared_hours::Number,
                                        relative_destination::Bool)

    spawns_per_meter_squared_seconds = KMSquaredHoursstoMSquaredSeconds(spawns_per_km_squared_hours)
    spawns_per_seconds = spawns_per_meter_squared_seconds * getArea(sources)
    queues = zeros(length(sources.shapes))
    return QueuedSpawnController(sources, destinations, queues, spawns_per_seconds, relative_destination)
end


# must return a vector of Tuple of cartesian 2 points
function getSourceAndDestinations(sc::QueuedSpawnController, timestep::Number, current_time::Number, aircraft::Vector{Aircraft}, ego_position::Cartesian2, rng::AbstractRNG)
    # foind how many to spawn this timestep
    ac_to_spawn = makeInt(sc.spawnrate_per_second * timestep, rng)
    ret = Vector{Tuple{Cartesian2, Cartesian2}}(undef, 0)

    
    # randomly add to queues based on priorities given in shape manager
    for i in 1:ac_to_spawn
        index = sampleShapeIndex(sc.sources, rng)
        sc.queues[index] += 1
    end
    
    # try to pull from queues based on if there is anyone around
    for i in 1:length(sc.queues)
        # if no one in queue, skip
        if sc.queues[i] == 0 
            continue
        end

        # sample starting point from the shape at this index
        # this will be where the person in queue spawns
        start = samplePoint(sc.sources.shapes[i], rng) + ego_position
        
        # verify there is no immediate NMAC
        if !(isAirspaceClear(start, aircraft))
            # println("Failed to spawn ", start, " becuase there is an ac")
            continue
        end
        
        # if not, then find their destination
        destination = samplePoint(sc.destinations, rng)
        if sc.relative_destination
            destination += start
        end

        # add to list, decrement queue
        push!(ret, (start, destination))
        sc.queues[i] -= 1
    end

    # return final list
    return ret
end

function setSpawnRate(sc::QueuedSpawnController, spawns_per_km_squared_hours::Number)
    spawns_per_meter_squared_seconds = KMSquaredHoursstoMSquaredSeconds(spawns_per_km_squared_hours)
    spawns_per_seconds = spawns_per_meter_squared_seconds * getArea(sc.sources)
    sc.spawnrate_per_second = spawns_per_seconds
end

function isAirspaceClear(point::Cartesian2, ac::Vector{Aircraft})
    for plane in ac
        if Magnitude(plane.dynamic.position - point) < 150.0 # lets assume 150 meters is too close for a ac taking off!
            return false
        end
    end

    return true
end


function render(sc::QueuedSpawnController, ax)
	# render the src and destination
    render(sc.sources, ax, "g", ":") # dotted line
	render(sc.destinations, ax, "b", ":") # dotted line

    # render queue counts
    for i in 1:length(sc.sources.shapes)
        if typeof(sc.sources.shapes[i]) == Circle
            x = sc.sources.shapes[i].center_point.x 
            y = sc.sources.shapes[i].center_point.y + sc.sources.shapes[i].radius
            s = string(sc.queues[i])
            plt.text(x, y, s)
        elseif typeof(sc.sources.shapes[i]) == Rectangle
            x = sc.sources.shapes[i].top_left.x - 10
            y = sc.sources.shapes[i].top_left.y + 10
            s = string(sc.queues[i])
            plt.text(x, y, s)
        else
            # TODO any other shapes you create must go here
            println("Shape not supported for queue rendering")
        end
    end
end
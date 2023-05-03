# dependencies: Cartesian2, AbstractShape, Circle, Rectangle

mutable struct ShapeManager
    shapes::Vector{AbstractShape}
    weights::Vector{Real}
    total_area::AbstractFloat
end

function ShapeManager()
    return ShapeManager([], [], 0.0)
end

function addShape!(sm::ShapeManager, s::AbstractShape, weight::Number=1)
    push!(sm.shapes, s)
    push!(sm.weights, weight)
    sm.total_area += getArea(s)
end

# O(n) runtime where n is number of shapes
function getNearestPointOnEdge(sm::ShapeManager, point::Cartesian2)
    nearest_point = nothing
    best_distance = Inf
    if sm != nothing
        for shape in sm.shapes
            some_point, some_distance = getNearestPointOnEdge(shape, point)
            if abs(some_distance) < abs(best_distance)
                nearest_point = some_point
                best_distance = some_distance
            end
        end
    end
    return nearest_point, best_distance
end


function samplePoint(sm::ShapeManager, rng)
    if length(sm.shapes) == 0
        error("No shapes to sample from")
    end
    
    # fetch a random shape
    some_shape = sample(rng, sm.shapes, Weights(sm.weights)) 

    # return random point in shape
    return samplePoint(some_shape, rng)
end

function sampleShapeIndex(sm::ShapeManager, rng)
    if length(sm.shapes) == 0
        error("No shapes to sample from")
    end
    
    # fetch a random shape
    index = sample(rng,  Weights(sm.weights)) 
    return index
end


function isEmpty(sm::ShapeManager)
    return length(sm.shapes) == 0
end


function getArea(sm::ShapeManager)
    return sm.total_area
end


# this function should use pyplot to plot the shape
# ax = the graph, look at other examples its complicated
# color = string such as "r", "g", see pyplot examples
# ls = line shape, such as "-", "--", ":", etc. see pyplot
function render(sm::ShapeManager, ax, color, ls)
    for shape in sm.shapes
		plotShape(shape, ax, color, ls) # dotted line
    end
end
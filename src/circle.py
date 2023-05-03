# depends on carteisan 2, AbstractShape.jl

# Additionally, it must define the following:
#   Relevant geometry - position, size, etc
#   Sampling distributions 
#   Clip = a bool of whether a sampled point is clipped to gurantee it is within the shape or not
#       For example, a standard normal distribution may be the internal sampling distribution, which can technically output a point from -inf to inf.
#       Therefore, we may want to clip the points to always be within the shape
struct Circle <: AbstractShape
    # geometry
    center_point::Cartesian2
    radius::AbstractFloat

    # distributions for sampling. Note we will call rand(your_distribution) to get a random value. See Distributions.jl for helpful ones.
    # Default distribution is uniform random
    r_distribution
    angle_distribution

    # to clip or not
    clip::Bool
end


function Circle(center_point::Cartesian2, 
                radius::AbstractFloat; 
                r_distribution=Uniform(0.0, radius), 
                angle_distribution=Uniform(0.0, 2pi), 
                clip=false
                )
    @assert radius >= 0.0
    return Circle(center_point, radius, r_distribution, angle_distribution, clip)
end


# This function finds the nearest point to "point" along the edge of the shape s. 
# it also returns the distance from that point to the nearest point. If the point is outside the shape, the distance is positive
# if the point is inside the shape, the distance is negative
function getNearestPointOnEdge(S::Circle, point::Cartesian2)
    # get vector from our point to center of circle
    vector = S.center_point - point

    # get distance
    distance_to_center = Magnitude(vector) # positive always
    distance_to_edge = distance_to_center - S.radius # positive if outside, negative if inside

    # get point
    unit_vector = vector * (1.0/ Magnitude(vector))
    edge_point = point + unit_vector * distance_to_edge
    
    return edge_point, distance_to_edge
end

# This function samples a point from the shape randomly. The internal distribution should be specified in the constructor of a given shape
# this should return a Cartesian2 point
# any randomness must use the RNG
# clip if Clip == true
function samplePoint(S::Circle, rng)
    # random radius and angle according to provided distros
    r = rand(rng, S.r_distribution)
    angle = rand(rng, S.angle_distribution)

    # clip
    if S.clip
        r = clip(r, -S.radius, S.radius)
        # note angle doesnt matter since they repeat basically and we are about to take sin and cos
    end

    # convert to x,y
    x = r * cos(angle)
    y = r * sin(angle)
    return Cartesian2(x + S.center_point.x, y + S.center_point.y)
end


# this function should use pyplot to plot the shape
function plotShape(S::Circle, ax, color, ls)
    circle1 = plt.Circle((S.center_point.x, S.center_point.y), S.radius, color=color, fill=false, ls=ls)
    ax.add_patch(circle1)
end

# this function returns the area of the shape.
# if the shape does not have a fixed border (IE for a gaussian distribution which can in theory return a point anywhere between -inf and inf)
# Then decide on a relevant size. Such as the area of which 95% of spawns will be or something like this
function getArea(S::Circle)
    return S.radius^2 * pi 
end
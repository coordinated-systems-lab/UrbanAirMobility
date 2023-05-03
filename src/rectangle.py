# depends on carteisan 2, AbstractShape.jl

# Additionally, it must define the following:
#   Relevant geometry - position, size, etc
#   Sampling distributions 
#   Clip = a bool of whether a sampled point is clipped to gurantee it is within the shape or not
#       For example, a standard normal distribution may be the internal sampling distribution, which can technically output a point from -inf to inf.
#       Therefore, we may want to clip the points to always be within the shape
struct Rectangle <: AbstractShape
    # geometry
    top_left::Cartesian2
    bottom_right::Cartesian2

    # distributions for sampling. Note we will call rand(your_distribution) to get a random value. See Distributions.jl for helpful ones.
    # Default distribution is uniform random
    x_distribution
    y_distribution

    # to clip or not
    clip::Bool
end


function Rectangle( top_left::Cartesian2, 
                    bottom_right::Cartesian2, 
                    x_distribution=Uniform(top_left.x, bottom_right.x), 
                    y_distribution=Uniform(bottom_right.y, top_left.y), 
                    clip=false
                  )
    @assert top_left.x  <= bottom_right.x
    @assert top_left.y  >= bottom_right.y

    return Rectangle(top_left, bottom_right, x_distribution, y_distribution, clip)
end


# This function finds the nearest point to "point" along the edge of the shape s. 
# it also returns the distance from that point to the nearest point. If the point is outside the shape, the distance is positive
# if the point is inside the shape, the distance is negative
function getNearestPointOnEdge(S::Rectangle, point::Cartesian2)
    x, y = nothing, nothing
    top = S.top_left.y
    bottom = S.bottom_right.y
    left = S.top_left.x
    right = S.bottom_right.x
    outside = false # whether or not our point is outside the rectangle. Defaults to false. If any dim is outside, then it becomes true. 

    # find nearest x value
    if point.x < left
        x = left
        outside = true
    elseif point.x > right
        x = right
        outside = true
    else
        x = point.x
    end

    # find nearest y value
    if point.y < bottom
        y = bottom
        outside = true
    elseif point.y > top
        y = top
        outside = true
    else
        y = point.y
    end

    # special case. If we are inside rectangle in both x and y, then the above didnt work
    if !outside
        # adjust x,y for inside point. This is kinda complex because we have to calculate triangles from the inside of the rectangle
        vector_back_slash = S.bottom_right - S.top_left # points from top left to bottom right like a back slash
        vector_forward_slash = Cartesian2(right - left, top - bottom) # points from bottom left to top right like a forward slash

        # make them unit length
        vector_back_slash = vector_back_slash *  (1.0/Magnitude(vector_back_slash))
        vector_forward_slash = vector_forward_slash *  (1.0/Magnitude(vector_forward_slash))

        # calculate which trinagle we are in. See diagram at bottom of file
        change_x = point.x - left
        y_value_of_slash_by_point =  (vector_forward_slash * (point.x / vector_forward_slash.x)).y + bottom
        above_forward_slash = point.y > y_value_of_slash_by_point
        
        change_x = point.x - left
        y_value_of_slash_by_point = (vector_back_slash * (point.x / vector_back_slash.x)).y + top
        above_backwards_slash = point.y > y_value_of_slash_by_point
        

        # now that we know which triangle we are in, can just calculate the x,y
        if above_forward_slash && above_backwards_slash # top triangle
            x = point.x
            y = top
        elseif above_forward_slash && !above_backwards_slash # left triangle
            x = left
            y = point.y
        elseif !above_forward_slash && above_backwards_slash # right triangle
            x = right
            y = point.y
        else # bottom triangle
            x = point.x
            y = bottom
        end
    end


    # create edge point. Find distance. If outside, leave it positive. If inside, make it negative
    edge_point = Cartesian2(x,y)
    distance_to_edge = Magnitude(point - edge_point)
    distance_to_edge = outside ? distance_to_edge : -distance_to_edge
    return edge_point, distance_to_edge
end

# This function samples a point from the shape randomly. The internal distribution should be specified in the constructor of a given shape
# this should return a Cartesian2 point
# any randomness must use the RNG
# clip if Clip == true
function samplePoint(S::Rectangle, rng)
    # random x and y according to provided distros
    x = rand(rng, S.x_distribution)
    y = rand(rng, S.y_distribution)

    # clip
    if S.clip
        x = clip(x, S.top_left.x, S.bottom_right.x)
        y = clip(y, S.bottom_right.y, S.top_left.y)
    end

    return Cartesian2(x, y)
end

# this function should use pyplot to plot the shape
function plotShape(S::Rectangle, ax, color, ls)
    circle1 = plt.Rectangle((S.top_left.x, S.bottom_right.y), S.bottom_right.x-S.top_left.x, S.top_left.y-S.bottom_right.y, color=color, fill=false, ls=ls)
    ax.add_patch(circle1)
end


# this function returns the area of the shape.
# if the shape does not have a fixed border (IE for a gaussian distribution which can in theory return a point anywhere between -inf and inf)
# Then decide on a relevant size. Such as the area of which 95% of spawns will be or something like this
function getArea(S::Rectangle)
    return (S.bottom_right.x - S.top_left.x) * (S.top_left.y - S.bottom_right.y)
end


#= Diagram for nearest point. Consider the following
    solid lines are the borders of the rectangle. Dotted lines denote regions of interest where the behavior of nearest point is consistent
    note the forward and backwards slashes (in dots) inside the rectangle
        .                     .
        .                     .
        .                     .
....... ______________________ ...............
        |  .               .  |
        |     .         .     |        
        |         . .         |
        |         . .         |
        |      .       .      |
        |   .             .   |
........|_____________________|................
        .                     .
        .                     .        
        .                     .
        
=#
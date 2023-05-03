function getLineOfPoints(start::Cartesian2, dest::Cartesian2, number_points::Int; bidirectional::Bool=false, start_index::Int=0)
    @assert number_points >= 0

    # generate all the points, evenly distrubted
    xs = LinRange(start.x, dest.x, number_points + 2)
    ys = LinRange(start.y, dest.y, number_points + 2)

    points = Vector{Cartesian2}(undef, 0)
    edges = Vector{Edge{Int64}}(undef, 0)

    # create points
    for i in 1:length(xs)
        push!(points, Cartesian2(xs[i], ys[i]))
    end

    # create edges
    for i in 1:length(xs)-1
        current = i + start_index
        next = i + 1 + start_index
        push!(edges, Edge(current, next))
        if bidirectional
            push!(edges, Edge(next, current))
        end
    end

    return points, edges
end


# a convenience function that returns a circle of points that are connected. 
# optionally connected in both directions, defaults to false
function getCircleOfPoints(center_point::Cartesian2, radius::AbstractFloat, number_points::Int; 
                            connected_clockwise::Bool=false, connected_counter_clockwise::Bool=false, start_index::Int=0)
    @assert number_points > 0
    @assert connected_clockwise || connected_counter_clockwise

    # generate all the points, evenly distrubted
    thetas = LinRange(0.0, 2pi,  number_points+1)
    thetas = thetas[1:end-1]

    points = Vector{Cartesian2}(undef, 0)
    edges = Vector{Edge{Int64}}(undef, 0)

    # create points
    for i in 1:length(thetas)
        x = radius * cos(thetas[i])
        y = radius * sin(thetas[i])
        push!(points, Cartesian2(x, y) + center_point)
    end

    # create edges
    num_points = length(points)
    for i in 1:num_points
        current = i + start_index
        next = i + 1 > num_points ? 1 : i + 1
        next += start_index
        if connected_counter_clockwise
            push!(edges, Edge(current, next))
        end
        if connected_clockwise
            push!(edges, Edge(next, current))
        end
    end

    return points, edges
end

# a convenience function that returns a rectangle of points that are connected. 
# note the number of rows and cols is inside the rectange, IE if they are 0, this will generate the outside edge
# every row/col is 1-directional, alternates which direction
function getRectangleOfPoints(top_left::Cartesian2, bottom_right::Cartesian2, number_rows::Int, number_cols::Int; start_index::Int=0)
    @assert number_rows >= 0 && number_cols >= 0
    @assert number_rows % 2 == 0 && number_cols % 2 == 0

    # generate all the points, evenly distrubted
    points = Vector{Cartesian2}(undef, 0)
    edges = Vector{Edge{Int64}}(undef, 0)

    # generate all the points, evenly distrubted
    xs = LinRange(top_left.x, bottom_right.x, number_cols + 2)
    ys = LinRange(bottom_right.y, top_left.y, number_rows + 2)

    # create points
    for y in ys
        for x in xs
            push!(points, Cartesian2(x, y))
        end
    end

    # create edges
    for row in 1:(number_rows+2)
        for col in 1:(number_cols+2)
           
            # find index of current point. This function may not be only points in list,
            # so add start index also.
            this_index = start_index + col + (row-1) * (number_cols + 2)

            # add direction based on row index
            if row % 2 == 0 && col != 1
                push!(edges, Edge(this_index, this_index - 1))
            elseif row % 2 == 1 && col != number_cols+2
                push!(edges, Edge(this_index, this_index + 1))
            end

            # add direction based on col index
            if col % 2 == 0 && row != number_rows+2
                push!(edges, Edge(this_index, this_index + (number_cols + 2) ))
            elseif col % 2 == 1 && row != 1
                push!(edges, Edge(this_index, this_index - (number_cols + 2) ))
            end
            
        end
    end

    return points, edges
end
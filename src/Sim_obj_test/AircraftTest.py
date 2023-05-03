error = 0.001

# Test 1
t1 = Aircraft(  Dynamics(Cartesian2(0.0,0.0), Polar2(0.0,0.0), Polar2(0.0,0.0)), 
                Cartesian2(10.0,0.0), 
                Polar2(5.0, pi),
                10.0,
                100.0)
setAcceleration!(t1, Polar2(10000, 2pi))
@assert t1.dynamic.acceleration.r == 5.0
@assert t1.dynamic.acceleration.θ == pi

# Test 2
t1 = Aircraft(  Dynamics(Cartesian2(0.0,0.0), Polar2(0.0,0.0), Polar2(0.0,0.0)), 
                Cartesian2(10.0,0.0), 
                Polar2(5.0, pi),
                10.0,
                100.0)
@assert hasArrived(t1, 100) == (true, true)
@assert hasArrived(t1, 1) == (false, false)

# Test 3
t1 = Aircraft(  Dynamics(Cartesian2(0.0,0.0), Polar2(0.0,0.0), Polar2(0.0,0.0)), 
                [Cartesian2(10.0,0.0), Cartesian2(1000.0,0.0)], 
                Polar2(5.0, pi),
                10.0,
                100.0)
@assert hasArrived(t1, 100) == (true, false)

println("Passed AircraftTest")
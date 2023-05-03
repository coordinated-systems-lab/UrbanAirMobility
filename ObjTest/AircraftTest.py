error = 0.001


#Test1
t1 = Aircraft(Dynamics(Cartesian2(0,0),Polar2(0,0),Polar2(0,0),),
              Cartesian2(10,0),
              Polar2(5,np.pi),
              10,
              100)


setAcceleration(t1,Polar2(10_000, 2 * np.pi))

assert t1.dynamics.acceleration.r == 5
assert t1.dynamics.acceleration.theta == np.pi

#Test2
t1 = Aircraft(Dynamics(Cartesian2(0,0),Polar2(0,0),Polar2(0,0),),
              Cartesian2(10,0),
              Polar2(5,np.pi),
              10,
              100)

assert hasArrived(t1,100) == (True,True)
assert hasArrived(t1,1) == (False, False)

#Test3
t1 = Aircraft(Dynamics(Cartesian2(0,0),Polar2(0,0),Polar2(0,0),),
              Cartesian2(10,0),
              Polar2(5,np.pi),
              10,
              100)

assert hasArrived(t1,100) == (True,False)

print('Passed AircraftTest')
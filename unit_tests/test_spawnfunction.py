#Test 1


import cartesian2 as c2 
import spawnfunction as spwnfnc

b = c2.Cartesian2(1000,1000)


for _ in range(100):
    start, dest = spwnfnc.ego_spawn_function(b, c2.Cartesian2(0,0),0,100)
    assert 0 <= start.x <= b.x
    assert 0 <= start.y <= b.y
    assert c2.Cartesian2.__abs__(start - dest) - 5000 < 0.1

print('Passed spawnfunction')
 
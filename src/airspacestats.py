class AirspaceStats:
    def __init__(self,time = [],number_aircraft = [],number_NMAC = [],arrived_ac) = []:
        self.time = time
        self.number_aircraft = number_aircraft
        self.arrived_ac = arrived_ac
        self.number_NMAC = number_NMAC
    
    def add_stats(self,current_time, current_num_ac, nmac_this_timestep, list_ac):
        self.time.append(current_time)
        self.number_aircraft.append(current_num_ac)
        self.number_NMAC.append(nmac_this_timestep)
        self.arrived_ac.append(list_ac)
    
    def average_normalized_route_length(self):
        num_ac = 0
        route_len = 0 #this variable was named "len" in julia
        for items in self.arrived_ac:
            for ac in items:
                route_len += getNormalizedRouteLength(ac.stats)
                num_ac += 1
        return route_len/num_ac
                
    def average_num_nmac_per_second_for_arrived_ac(self):
        num_ac = 0
        num_nmac_per_second = 0
        
        for items in self.arrived_ac:
            for ac in items:
                num_nmac_per_second += getNMACPerSecond(ac.stats)
                num_ac += 1
        return num_nmac_per_second/num_ac
    
    def average_num_nmac_per_second_for_airspace(self, timestep):
        total_flight_time = sum(self.number_aircraft) * timestep
        total_nmac = sum(self.number_NMAC)
        return total_nmac/total_flight_time
    

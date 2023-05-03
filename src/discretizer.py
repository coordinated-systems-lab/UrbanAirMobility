import numpy as np
import math 
def getDiscreteFunctions(state_space, numberBins):

    def getState(s):

        dimensionIndicies = [] ## need to undertsand this line, also convert from list to ndarray for faster performance 
        for i in range(len(state_space)):
            width = (state_space[i].right - state_space[i].left) / numberBins[i]
            dim = math.floor((s[i] - state_space[i].left) / width) +1
            dimensionIndicies.append(dim)

        index = 1 
        for i in range(len(state_space)):
            offset = 1 
            j = i-1 
            while j > 0:
                offset *= numberBins[j]
                j -= 1
            index += (dimensionIndicies[i] - 1 ) * offset
        return index
    
    numberStates = 1 
    for value in numberBins:
        numberStates *= value
    return getState # missing output need to understand julia Base.OneTo
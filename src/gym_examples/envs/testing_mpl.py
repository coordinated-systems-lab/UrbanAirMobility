import matplotlib.pyplot as plt
import numpy as np 


x = np.linspace(0, 2*np.pi, num=200)
y = np.sin(x)

## Using subplots for drawing figure and axes(aka subplot) at the same time
fig, subplot = plt.subplots()

subplot.plot(x,y)
plt.show()

## Separating fig and axes(aka subplots)
fig = plt.figure(figsize=(2,2), facecolor='lightskyblue', #* figsize -> the method desc says figsize is a sequence, what is this sequence
                 layout='constrained')

ax = fig.add_subplot()

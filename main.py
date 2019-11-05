"""
This file runs Quadtree code
Created: April 13, 2019
Last Edited: April 15, 2019
By Bill
"""

import Quadtree as qt
import Gravity as gr
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt


size = 11
mass = 1
number = 100

t = 1
G = 0.1
epsilon = 0.01

dt = 1e-3
steps = 200
interval = 1

particles = np.random.rand(number, 2) + 5 * np.ones([number, 2])

# theta = np.linspace(0, 1.8 * np.pi, number)
# particles = np.array([0.4 * np.sin(theta) + 0.5, 0.4 * np.cos(theta) + 0.5])
# particles = particles.T

massList = mass * np.ones(number)
velocityList = np.zeros([number, 2])

qtree = qt.Quadtree(size)
qtree.generate(particles, massList)
gravities = gr.updateGravity(size, particles, massList, t, G, epsilon)
print(gravities)

# qtree.stringShow()
qtree.figureShow()

fig, ax = plt.subplots()
data = [particles]

for step in range(steps):
    gravityList = gr.updateGravity(size, particles, massList, t, G, epsilon)
    [particles, velocityList] = gr.updateEuler(particles, velocityList, gravityList, dt)

    if (step + 1) % interval == 0:
        data.append(deepcopy(particles))

    if (step + 1) % (10 * interval) == 0:
        print("Step ", step + 1, "/", steps)

for frame in range(0, len(data)):
    ax.cla()
    particles = data[frame].T
    ax.plot(particles[0], particles[1], ".r")
    ax.set_title("Step {}".format(frame * interval))
    ax.set_aspect(1)
    plt.xlim([0, size])
    plt.ylim([0, size])
    plt.pause(0.01)

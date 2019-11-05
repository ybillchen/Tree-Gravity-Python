"""
This file calculates gravity
Created: April 15, 2019
Last Edited: April 15, 2019
By Bill
"""

import Quadtree as qt
import numpy as np


def dist2(location1, location2):
    vector = location1 - location2
    return np.sum(np.square(vector))


def gravityAcceleration(location1, mass1, location2, G, epsilon):
    vector = location1 - location2
    dist2 = np.sum(np.square(vector))
    dist = np.sqrt(dist2)

    acceleration = G * mass1 / (dist2 + np.square(epsilon))
    acceleration = acceleration * vector / dist

    return acceleration


def unitGravity(node, particle, theta, G, epsilon):
    """Calculates unit gravity"""

    if node.isLeaf == True:
        if node.inNode(particle) or len(node.location) == 0:
            return np.array([0, 0])
        else:
            return gravityAcceleration(node.location, node.mass, particle, G, epsilon)

    unitSize = node.size / pow(2, node.level)

    if np.square(unitSize) / dist2(node.location, particle) < np.square(theta):
        return gravityAcceleration(node.location, node.mass, particle, G, epsilon)
    else:
        gravitySum = np.array([0, 0])

        for index in range(0, 4):
            deltaGravity = unitGravity(node.children[index], particle, theta, G, epsilon)
            gravitySum = gravitySum + deltaGravity

        return gravitySum


def updateGravity(size, particles, massList, theta, G, epsilon):
    """Updates gravities"""

    qtree = qt.Quadtree(size)
    qtree.generate(particles, massList)

    length = len(particles)
    gravityList = np.zeros([length, 2])

    for index in range(0, length):
        gravityList[index] = unitGravity(qtree.root, particles[index], theta, G, epsilon)

    return gravityList

def updateEuler(particles, velocityList, accelerationList, dt):
    """Update locations and velocities via Euler method"""

    newParticles = dt * velocityList + particles
    newVelocityList = dt * accelerationList + velocityList

    return [newParticles, newVelocityList]

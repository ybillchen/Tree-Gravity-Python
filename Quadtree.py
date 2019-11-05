"""
This file defines Node and Quadtree classes
Created: April 13, 2019
Last Edited: April 15, 2019
By Bill
"""


from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt


class Node(object):
    """Node"""

    def __init__(self, size, level, i, j):
        self.isLeaf = True
        self.children = None
        self.mass = 0
        self.location = np.array([])
        self.size = size
        self.level = level
        self.i = i
        self.j = j

    # Node breeds

    def breeds(self):
        """Node breeds"""

        if self.isLeaf == False:
            return

        self.isLeaf = False
        self.children = [Node(self.size, self.level + 1, 2 * self.i, 2 * self.j),
                         Node(self.size, self.level + 1, 2 * self.i, 2 * self.j + 1),
                         Node(self.size, self.level + 1, 2 * self.i + 1, 2 * self.j),
                         Node(self.size, self.level + 1, 2 * self.i + 1, 2 * self.j + 1)]

        if len(self.location) == 0:
            return

        particle = deepcopy(self.location)

        for index in range(0, 4):
            if self.children[index].inNode(particle):
                self.children[index].location = particle
                self.children[index].mass = self.mass
                return

        return

    # Judge if particle is in node

    def inNode(self, particle):
        """Judge if particle is in node"""

        [particlei, particlej] = particle

        unitSize = self.size / pow(2, self.level)
        mini = self.i * unitSize
        maxi = mini + unitSize
        minj = self.j * unitSize
        maxj = minj + unitSize

        if particlei >= mini and particlei < maxi and particlej >= minj and particlej < maxj:
            return True

        return False

    # Add a particle to Node

    def addParticle(self, particle, mass):
        """Add a particle to Node"""

        if self.isLeaf == True:
            if len(self.location) == 0:
                self.location = particle
                self.mass = mass
                return

            self.breeds()

        # self.location = [(self.location[0] * self.mass + particle[0]) / (self.mass + mass),
        #                  (self.location[1] * self.mass + particle[1]) / (self.mass + mass)]
        self.location = (self.location * self.mass + particle * mass) / (self.mass + mass)
        self.mass = self.mass + mass

        for index in range(0, 4):
            if self.children[index].inNode(particle):
                self.children[index].addParticle(particle, mass)
                return

        return

    # Show Node

    def stringShow(self):
        """Show Node by string"""

        if len(self.location) == 0:
            print(self.level * "  |", "Level", self.level, "---", self.mass)
        else:
            print(self.level * "  |", "Level", self.level, "---", self.mass, "---", self.location)

        if self.isLeaf == True:
            return

        for index in range(0, 4):
            self.children[index].stringShow()

    def figureShow(self):
        """Show Node by figure"""

        lines = []

        if self.level == 0:
            lines.append([[0, 0], [0, self.size]])
            lines.append([[0, self.size], [0, 0]])
            lines.append([[self.size, 0], [self.size, self.size]])
            lines.append([[self.size, self.size], [self.size, 0]])

        if self.isLeaf == True:
            if len(self.location) == 0:
                pass
            else:
                lines.append([self.location.tolist()])

            return lines

        unitSize = self.size / pow(2, self.level)
        lines.append([[self.i * unitSize + (unitSize / 2), self.i * unitSize + (unitSize / 2)],
                      [self.j * unitSize, self.j * unitSize + unitSize]])
        lines.append([[self.i * unitSize, self.i * unitSize + unitSize],
                      [self.j * unitSize + (unitSize / 2), self.j * unitSize + (unitSize / 2)]])

        for index in range(0, 4):
            lines = lines + self.children[index].figureShow()

        return lines


class Quadtree(object):
    """Quadtree"""

    def __init__(self, size):
        self.root = Node(size, 0, 0, 0)

    # Generate Quadtree from particles

    def generate(self, particles, massList):
        """Generate Quadtree from particles"""

        length = len(particles)

        for index in range(0, length):
            self.root.addParticle(particles[index], massList[index])

    # Show Quadtree

    def stringShow(self):
        """Show Quadtree by string"""

        self.root.stringShow()

    def figureShow(self):
        """Show Quadtree by figure"""

        lines = self.root.figureShow()

        for line in lines:
            if len(line) == 2:
                plt.plot(line[0], line[1], "black")
            else:
                plt.plot(line[0][0], line[0][1], ".r")

        ax = plt.gca()
        ax.set_aspect(1)
        plt.show()

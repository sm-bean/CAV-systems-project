import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
ah = 0.2
bh = 0.4
k = -0.2912416558
a = 1
b1 = 0
b2 = 0
cccDelay = 0.5
humanDelay = 1

L = np.matrix([[0, 0, 0, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [-1, 1, 0, 0, 0, 0],
              [0, -1, 1, 0, 0, 0],
              [1, 0, -1, 0, 0, 0]])
P = np.matrix([[0, 0, 0, 0, 0, 0],
              [0, -(ah + bh), bh, 0, ah * k, 0],
              [bh, 0, -(ah + bh), 0, 0, ah * k],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]])
R = np.matrix([[-(a + b1 + b2), b1, b2, a * k, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]])
I = np.matrix([[1, 0, 0, 1, 0, 0],
              [0, 1, 0, 0, 1, 0],
              [0, 0, 1, 0, 0, 1],
              [1, 0, 0, 1, 0, 0],
              [0, 1, 0, 0, 1, 0],
              [0, 0, 1, 0, 0, 1]])

unitSquare = np.array([[-0.5, 0.5], [0.5, 0.5], [-0.5, -0.5], [0.5, -0.5]])

max = 2
min = -2
N = 3

def quarterSquare(square):
    sideLength = square[1][0] - square[0][0]
    scaledSquare = square*0.5
    return scaledSquare - (0.25*sideLength)

def makeMesh(square):
    sideLength = square[1][0] - square[0][0]
    quartersquare = quarterSquare(square)
    quartersquare2 = quartersquare.copy()
    quartersquare2[:, 0] += (sideLength/2)
    quartersquare3 = quartersquare.copy()
    quartersquare3[:, 1] += (sideLength/2)
    quartersquare4 = quartersquare.copy()
    quartersquare4 += (sideLength/2)
    return np.concatenate((quartersquare, quartersquare2, quartersquare3, quartersquare4), axis=0)

sideLength = (max - min) / N-1
wholeSquare = unitSquare*max*2
firstQuarter = quarterSquare(wholeSquare)
initialMesh = makeMesh(wholeSquare)
secondMesh = makeMesh
plt.plot(initialMesh[:, 0], initialMesh[:, 1], 'go')
plt.show()
nodes = []

#print(nodes)

def f(gamma):
    return np.linalg.det((gamma * I) - L - (P * (np.exp(1) ** (-gamma * humanDelay))) - (R * (np.exp(1) ** (-gamma * cccDelay))))

#print([f(gamma*1j) for gamma in range(100)])
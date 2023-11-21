import numpy as np
import matplotlib.pyplot as plt
import math
from copy import deepcopy
ah = 0.2
bh = 0.4
k = -0.2912416558
a = 1
b1 = 0
b2 = 0
cccDelay = 0.5
humanDelay = 1
fineness = 0.001

def f(gamma):
    return np.linalg.det((gamma * I) - L - (P * (np.exp(1) ** (-gamma * humanDelay))) - (R * (np.exp(1) ** (-gamma * cccDelay))))

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

"""def quarterSquare(square):
    sideLength = square[1][0] - square[0][0]
    scaledSquare = square*0.5
    return scaledSquare - (0.25*sideLength)"""

roots = []

def quarterSquare(square): # returns the top-left quarter square
    hsl = (square[1][0] - square[0][0])/2
    topLeft = square[0]
    topRight = square[1]
    topRight[0] -= hsl
    bottomLeft = square[2]
    bottomLeft[1] += hsl
    bottomRight = square[3]
    bottomRight[0] -= hsl
    bottomRight[1] += hsl
    return np.array([topLeft, topRight, bottomLeft, bottomRight])

def makeMesh(square):
    sideLength = square[1][0] - square[0][0]
    quartersquare = quarterSquare(square)
    quartersquare2 = quartersquare.copy()
    quartersquare2[:, 0] += (sideLength/2)
    quartersquare3 = quartersquare.copy()
    quartersquare3[:, 1] -= (sideLength/2)
    quartersquare4 = quartersquare.copy()
    quartersquare4[:, 0] += (sideLength/2)
    quartersquare4[:, 1] -= (sideLength/2)
    return np.array([quartersquare, quartersquare2, quartersquare3, quartersquare4])

def plot(mesh):
    meshToPlot = mesh.reshape(-1, 2)
    rootsnp = np.array(roots)
    plt.plot(meshToPlot[:, 0], meshToPlot[:, 1], 'ro', markersize=2)
    plt.plot(rootsnp[:, 0], rootsnp[:, 1], 'bo', markersize=2)
    plt.show()

wholeSquare = unitSquare*max*2
initialMesh = makeMesh(wholeSquare)

finished = False
while not finished:
    
    for position,square in enumerate(initialMesh):

        realChanged = False
        imaginaryChanged = False
        reals = []
        imags = []

        for node in square:
            value = f(node[0] + node[1]*1j)
            reals.append(value.real)
            imags.append(value.imag)

            if (np.absolute(value)) < fineness:
                newMesh = np.delete(initialMesh, position, axis=0)
                root = [node[0], node[1]]
                roots.append(root)

        if not(all(i >= 0 for i in reals) or all(i < 0 for i in reals)):
            realChanged = True

        if not(all(i >= 0 for i in imags) or all(i < 0 for i in imags)):
            imaginaryChanged = True

        if (imaginaryChanged and realChanged):
            newSquares = makeMesh(square)
            initialMesh = np.concatenate((initialMesh, newSquares), axis=0)
            #print(initialMesh)
            #print(newSquares)
            #print("CHANGED!") # further split square
        
        else:
            #print(square) # omit square
            newMesh = np.delete(initialMesh, position, axis=0)
    plot(initialMesh)
            
plot(initialMesh)  

#print([f(gamma*1j) for gamma in range(100)])
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
    return np.array([quartersquare3, quartersquare4, quartersquare, quartersquare2])

sideLength = (max - min) / N-1
wholeSquare = unitSquare*max*2
firstQuarter = quarterSquare(wholeSquare)
initialMesh = makeMesh(wholeSquare)
secondMesh = makeMesh
#print(initialMesh)
#plt.plot(initialMesh[:, 0], initialMesh[:, 1], 'go')
plt.show()
nodes = []

for square in initialMesh:
    realChanged = False
    imaginaryChanged = False
    reals = []
    imags = []

    for node in square:
        value = f(node[0] + node[1]*1j)
        #print(value)
        reals.append(value.real)
        imags.append(value.imag)
    #print(reals)
    #print(imags)

    if not(all(i >= 0 for i in reals) or all(i < 0 for i in reals)):
        realChanged = True

    if not(all(i >= 0 for i in imags) or all(i < 0 for i in imags)):
        imaginaryChanged = True

    if (imaginaryChanged and realChanged):
        print("CHANGED!") # further split square
    else:
        print(square) # omit square
        np.delete(initialMesh, square)
        
    
#print(nodes)

#print([f(gamma*1j) for gamma in range(100)])
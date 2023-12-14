import math
import matplotlib.pyplot as plt
import pygame, sys
from statistics import stdev
import csv

reactionTime = 1
cccDelay = 0.2
ah = 0.4
bh = 0.2
alpha = 2
beta = 0.2
vmax = 30
hst = 5
hgo = 55
car_length = 5
track_length = 360
c = 0.05
amin = -6
amax = 3
stepsPerSecond = 50
speedOfAnimation = 5
StabilityThreshold = 3


class Car:
    cars = []

    def __init__(self, position, specificvmax):
        # currently all parameters are constant, but these can be changed per vehicle
        self.vmax = specificvmax
        self.amax = amax
        self.amin = amin
        self.hst = hst
        self.hgo = hgo
        self.car_length = car_length
        self.c = c
        self.reactionTime = reactionTime
        self.cccDelay = cccDelay

        self.headwayHistoryTau = [
            0 for x in range(round(stepsPerSecond * self.reactionTime))
        ]
        self.velocityHistoryTau = [
            0 for x in range(round(stepsPerSecond * self.reactionTime))
        ]
        self.headwayHistorySigma = [
            0 for x in range(round(stepsPerSecond * self.cccDelay))
        ]
        self.velocityHistorySigma = [
            0 for x in range(round(stepsPerSecond * self.cccDelay))
        ]
        self.distance_travelled = position
        self.velocity = 0

    def sort_cars():
        for i in range(len(Car.cars) - 1):
            for j in range(len(Car.cars) - 1):
                if Car.cars[j].distance_travelled > Car.cars[j + 1].distance_travelled:
                    temp = Car.cars[j + 1]
                    Car.cars[j + 1] = Car.cars[j]
                    Car.cars[j] = temp

        Car.cars.reverse()
        for human in Car.cars:
            print(human.distance_travelled)

    def selectCarInFront(self, car_in_front):
        self.next_vehicle = car_in_front

    def getHeadway(self):
        if self.next_vehicle == Car.cars[-1]:
            x = (
                self.next_vehicle.distance_travelled
                + track_length
                - self.distance_travelled
            ) - self.car_length

        else:
            x = (
                self.next_vehicle.distance_travelled - self.distance_travelled
            ) - self.car_length

        while x < 0:
            x += track_length
        return x

    def getPosition(self):
        return self.distance_travelled % track_length

    def updateVelocity(self):
        self.velocityHistoryTau.insert(0, self.velocity)
        self.velocityHistorySigma.insert(0, self.velocity)
        self.velocityHistoryTau.pop()
        self.velocityHistorySigma.pop()
        self.velocity += self.getAcceleration() / stepsPerSecond
        return self.velocity

    def getAcceleration(self):
        a = self.optimalAcceleration() + self.velocityDelta()
        if a <= self.amin - self.c:
            return self.amin
        elif a < self.amin + self.c:
            return a + ((self.amin - a + self.c) ** 2 / (4 * self.c))
        elif a <= self.amax - self.c:
            return a
        elif a < self.amax + self.c:
            return a - ((self.amax - a - self.c) ** 2 / (4 * self.c))
        else:
            return self.amax

    def getHeadwayTau(self):
        return self.headwayHistoryTau[-1]

    def getVelocityTau(self):
        return self.velocityHistoryTau[-1]

    def getHeadwaySigma(self):
        return self.headwayHistorySigma[-1]

    def getVelocitySigma(self):
        return self.velocityHistorySigma[-1]


class Human(Car):
    def __init__(self, position, humanspecificvmax=vmax):
        self.ah = ah
        self.bh = bh
        self.type = "human"
        Car.__init__(self, position, humanspecificvmax)

    def optimalVelocity(self):
        headway = self.getHeadwayTau()
        if headway <= self.hst:
            return 0
        elif headway >= self.hgo:
            return self.vmax
        elif (headway > self.hst) and (headway < self.hgo):
            return (self.vmax / 2) * (
                1 - (math.cos(math.pi * (headway - self.hst) / (self.hgo - self.hst)))
            )

    def optimalAcceleration(self):
        return self.ah * (self.optimalVelocity() - self.getVelocityTau())

    def velocityDelta(self):
        return self.bh * (self.next_vehicle.getVelocityTau() - self.getVelocityTau())

    def __str__(self):
        x = self.optimalVelocity()
        return f"Human OV - {self.optimalVelocity()}"


class Autonomous(Car):
    def __init__(self, position, autonomousspecificvmax=vmax):
        self.alpha = alpha
        self.beta = beta
        self.carsSeen = []
        self.type = "autonomous"
        Car.__init__(self, position, autonomousspecificvmax)

    def cascade(self):
        selfIndex = Car.cars.index(self)
        counter = selfIndex - 1
        if self.next_vehicle.type == "human":
            while Car.cars[counter].type == "human":
                self.carsSeen.append(counter)
                if counter == (len(Car.cars) - 1):
                    counter = 0
                else:
                    counter -= 1
            self.carsSeen.append(counter)
        else:
            self.carsSeen.append(counter)

    def optimalVelocity(self):
        headway = self.getHeadwaySigma()
        if headway <= self.hst:
            return 0
        elif headway >= self.hgo:
            return self.vmax
        else:
            return (self.vmax / 2) * (
                1 - (math.cos(math.pi * (headway - self.hst) / (self.hgo - self.hst)))
            )

    def optimalAcceleration(self):
        return self.alpha * (self.optimalVelocity() - self.getVelocitySigma())

    def velocityDelta(self):  # different velocity delta for autonomous vehicles
        tempDelta = 0
        for human_index in self.carsSeen:
            if Car.cars[human_index].type == "human":
                tempDelta = tempDelta + (
                    Car.cars[human_index].bh
                    * (
                        Car.cars[human_index].getVelocitySigma()
                        - self.getVelocitySigma()
                    )
                )
            elif Car.cars[human_index].type == "autonomous":
                tempDelta = tempDelta + (
                    Car.cars[human_index].beta
                    * (
                        Car.cars[human_index].getVelocitySigma()
                        - self.getVelocitySigma()
                    )
                )
        return tempDelta

    def __str__(self):
        x = self.optimalVelocity()
        return f"AUTOMATED OV - {self.optimalVelocity()}"


def linkCars():
    for i in range(len(Car.cars) - 1):
        Car.cars[i + 1].selectCarInFront(Car.cars[i])
    Car.cars[0].selectCarInFront(Car.cars[-1])
    for car in Car.cars:
        print(car.next_vehicle)
    for i in range(len(Car.cars) - 1):
        if Car.cars[i].type == "autonomous":
            Car.cars[i].cascade()


def main():
    counter = 0
    headwayData = []
    tempHeadway = []
    velocityData = []
    tempVelocity = []
    tempVelocityA, velocityA = [], []
    tempHeadwayA, headwayA = [], []
    tempAccelA, accelA = [], []
    accelData = []
    tempAccel = []
    tempPosition = []
    global positionData
    positionData = []
    stdevs = []
    finished = False

    fig, ax = plt.subplots(
        ncols=1, nrows=3, figsize=(10, 5.4), layout="constrained", sharex=True
    )

    while True:
        for x in range(stepsPerSecond):
            counter += 1
            for car in Car.cars:
                if car.type == "human":
                    tempVelocity.append(car.velocity)
                    tempAccel.append(car.getAcceleration())
                    tempHeadway.append(car.getHeadway())
                elif car.type == "autonomous":
                    tempVelocityA.append(car.velocity)
                    tempAccelA.append(car.getAcceleration())
                    tempHeadwayA.append(car.getHeadway())
                tempPosition.append(car.distance_travelled % track_length)

                car.updateVelocity()
                # print(f"pos: {round(car.distance_travelled%360)}")
                # print(f"v: {round(car.velocity)}")
                # print(f"ov: {round(car.optimalVelocity(vmax, hst, hgo))}")
                # print(f"a: {round(car.getAcceleration())}")
                car.distance_travelled += car.velocity / stepsPerSecond
                car.headwayHistoryTau.insert(0, car.getHeadway())
                car.headwayHistorySigma.insert(0, car.getHeadway())
                car.headwayHistoryTau.pop()
                car.headwayHistorySigma.pop()

                if car.getHeadway() < car.car_length:
                    print(f"CRASH DETECTED at {(counter*stepsPerSecond) + x} timesteps")
                    finished = True

            velocityData.append(tempVelocity)
            accelData.append(tempAccel)
            headwayData.append(tempHeadway)
            positionData.append(tempPosition)
            velocityA.append(tempVelocityA)
            headwayA.append(tempHeadwayA)
            accelA.append(tempAccelA)

            stdevs.append(stdev(tempHeadway + tempHeadwayA))

            if stdev(tempHeadwayA + tempHeadway) < StabilityThreshold:
                print(
                    f"ROBUST STABILITY ACHIEVED AT {(counter*stepsPerSecond) + x} timesteps"
                )
                finished = True

            tempHeadwayA = []
            tempAccelA = []
            tempVelocityA = []
            tempAccel = []
            tempVelocity = []
            tempPosition = []
            tempHeadway = []
        usr = input()
        if usr == "show" or finished:
            ax[0].plot(range(counter), velocityData)
            ax[0].plot(range(counter), velocityA, linestyle="dashed")
            ax[0].set_ylabel("Velocity")
            ax[1].plot(range(counter), accelData)
            ax[1].plot(range(counter), accelA, linestyle="dashed")
            ax[1].set_ylabel("Acceleration")
            ax[2].plot(range(counter), headwayData)
            ax[2].plot(range(counter), headwayA, linestyle="dashed")
            ax[2].plot(range(counter), stdevs, linewidth=3)
            ax[2].set_ylabel("Headway")
            plt.xlabel("Timesteps")
            plt.show()
            animate()
        elif usr == "end":
            animate()
        elif usr == "data":
            allVelocities = [
                vsHuman + vsAuto for vsHuman, vsAuto in zip(velocityData, velocityA)
            ]
            velocityHeaders = [
                f"Velocity{x+1}" for x in range(len(velocityData[0]))
            ] + [f"VelocityAV{x+1}" for x in range(len(velocityA[0]))]
            allAccels = [asHuman + asAuto for asHuman, asAuto in zip(accelData, accelA)]
            accelHeaders = [f"Accel{x+1}" for x in range(len(velocityData[0]))] + [
                f"AccelAV{x+1}" for x in range(len(velocityA[0]))
            ]
            allHeadways = [
                hsHuman + hsAuto for hsHuman, hsAuto in zip(headwayData, headwayA)
            ]
            headwayHeaders = [f"Headway{x+1}" for x in range(len(headwayData[0]))] + [
                f"HeadwayAV{x+1}" for x in range(len(velocityA[0]))
            ]

            with open("CAV_data.csv", "w", newline="") as cavData:
                dataWriter = csv.writer(cavData)

                headers = (
                    ["Time"]
                    + velocityHeaders
                    + accelHeaders
                    + headwayHeaders
                    + ["StdDV(Headway)"]
                )
                dataWriter.writerow(headers)

                for x in range(len(velocityData)):
                    row = (
                        [x / stepsPerSecond]
                        + allVelocities[x]
                        + allAccels[x]
                        + allHeadways[x]
                        + [stdevs[x]]
                    )
                    dataWriter.writerow(row)

        print([str(x) for x in Car.cars])


Car.cars = [Human(15, 20), Autonomous(45, 15), Autonomous(85)]

Car.sort_cars()
linkCars()


def animate(speed=speedOfAnimation):
    pygame.init()

    class humanSprite:
        def __init__(self, position, colour):
            self.x, self.y = position
            self.colour = colour

        def display(self):
            pygame.draw.circle(screen, self.colour, (self.x, self.y), 30, width=0)

    clock = pygame.time.Clock()

    screen_width = 720
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))

    humanSprites = [
        humanSprite((0, 0), "RED")
        if car.type == "human"
        else humanSprite((0, 0), "BLUE")
        for car in Car.cars
    ]

    bg = pygame.image.load("RingRoad.png")
    bg = pygame.transform.scale(bg, (screen_width, screen_height))
    r = 300
    for timestepsPassed in range(len(positionData) - 1):
        if timestepsPassed % speed == 0:
            screen.blit(bg, (0, 0))
        else:
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for pos, humanCar in enumerate(humanSprites):
            theta = (360 / track_length) * positionData[timestepsPassed][pos]
            humanCar.x, humanCar.y = (
                r * math.cos(math.radians(theta)) + 360,
                720 - ((r * math.sin(math.radians(theta)) + 360)),
            )
            humanCar.display()

        pygame.display.flip()
        clock.tick(60)
    exit()


main()

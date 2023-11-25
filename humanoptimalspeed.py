import math
import matplotlib.pyplot as plt
import pygame, sys

ah = 0.2
bh = 0.5
vmax = 5
hst = 5
hgo = 55
car_length = 5
track_length = 360
c = 0.03
amin = -20
amax = 3
stepsPerSecond = 100


class Car:
    cars = []

    def sort():
        for i in range(len(Car.cars) - 1):
            for j in range(len(Car.cars) - 1):
                if Car.cars[j].distance_travelled > Car.cars[j + 1].distance_travelled:
                    temp = Car.cars[j + 1]
                    Car.cars[j + 1] = Car.cars[j]
                    Car.cars[j] = temp

        Car.cars.reverse()


class Human:
    def __init__(self, position):
        self.distance_travelled = position
        self.velocity = 0

    def selectCarInFront(self, car_in_front):
        self.next_vehicle = car_in_front

    def getHeadway(self):
        if self.next_vehicle == Car.cars[-1]:
            x = (
                self.next_vehicle.distance_travelled
                + track_length
                - self.distance_travelled
            ) - car_length

        else:
            x = (
                self.next_vehicle.distance_travelled - self.distance_travelled
            ) - car_length

        while x < 0:
            x += track_length
        return x

    def getPosition(self):
        return self.distance_travelled % 360

    def optimalVelocity(self, ah, bh, vmax, hst, hgo):
        headway = self.getHeadway()
        if headway <= hst:
            return 0
        elif headway >= hgo:
            return vmax
        else:
            return (vmax / 2) * (
                1 - (math.cos(math.pi * (headway - hst) / (hgo - hst)))
            )

    def updateVelocity(self):
        self.velocity += self.getAcceleration()
        return self.velocity

    def optimalAcceleration(self, vstart):
        return (self.optimalVelocity(ah, bh, vmax, hst, hgo) - vstart) / stepsPerSecond

    def getAcceleration(self):
        a = self.optimalAcceleration(self.velocity)
        if a <= amin - c:
            return amin
        elif a < amin + c:
            return a + ((amin - a + c) ** 2 / (4 * c))
        elif a <= amax - c:
            return a
        elif a < amax + c:
            return a - ((amax - a - c) ** 2 / (4 * c))
        else:
            return amax

    def __str__(self):
        x = self.optimalVelocity(ah, bh, vmax, hst, hgo)
        return f"i_x is {self.distance_travelled % 360}, delta_s is {self.distance_travelled}, OV {x}"


def linkCars():
    for i in range(len(Car.cars) - 1):
        Car.cars[i + 1].selectCarInFront(Car.cars[i])
    Car.cars[0].selectCarInFront(Car.cars[-1])


def main():
    counter = 0
    velocityData = []
    tempVelocity = []
    accelData = []
    tempAccel = []
    tempPosition = []
    global positionData
    positionData = []
    fig, ax = plt.subplots(
        ncols=1, nrows=2, figsize=(10, 5.4), layout="constrained", sharex=True
    )
    while True:
        for x in range(stepsPerSecond):
            counter += 1
            for car in Car.cars:
                tempVelocity.append(car.velocity)
                tempAccel.append(car.getAcceleration())
                tempPosition.append(car.distance_travelled % 360)
                car.updateVelocity()
                # print(f"pos: {round(car.distance_travelled%360)}")
                # print(f"v: {round(car.velocity)}")
                # print(f"ov: {round(car.optimalVelocity(ah, bh, vmax, hst, hgo))}")
                # print(f"a: {round(car.getAcceleration())}")
                car.distance_travelled += car.velocity
            velocityData.append(tempVelocity)
            accelData.append(tempAccel)
            positionData.append(tempPosition)
            tempAccel = []
            tempVelocity = []
            tempPosition = []
        usr = input()
        if usr == "show":
            ax[0].plot([x for x in range(counter)], velocityData)
            ax[0].set_ylabel("Velocity")
            ax[1].plot([x for x in range(counter)], accelData)
            ax[1].set_ylabel("Acceleration")
            plt.xlabel("Timesteps")
            plt.show()
            break
        elif usr == "end":
            break

        print([str(x) for x in Car.cars])


Car.cars = [Human(350), Human(20), Human(50), Human(0)]

# print(humans[0].getPosition())

Car.sort()
linkCars()
main()

# Animation starts here
# print(positionData)
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

humanSprites = [humanSprite((0, 0), "RED") for car in Car.cars]
humanCar = humanSprite((0, 0), "RED")

bg = pygame.image.load("RingRoad.png")
bg = pygame.transform.scale(bg, (screen_width, screen_height))
r = 300
timestepsPassed = 0
for x in range(len(positionData) - 1):
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for pos, humanCar in enumerate(humanSprites):
        theta = positionData[x][pos]
        humanCar.x, humanCar.y = (
            r * math.cos(math.radians(theta)) + 360,
            720 - ((r * math.sin(math.radians(theta)) + 360)),
        )
        humanCar.display()
        timestepsPassed += 1

    pygame.display.flip()
    clock.tick(30)

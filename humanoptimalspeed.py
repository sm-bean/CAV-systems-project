import math

ah = 0.2
bh = 0.4
vmax = 30
hst = 5
hgo = 55
car_length = 5
track_length = 360
class Human():
  def __init__(self, position):
    self.distance_travelled = position

  def selectCarInFront(self, car_in_front):
    self.next_vehicle = car_in_front
  
  def getHeadway(self):
    x = (self.next_vehicle.distance_travelled - self.distance_travelled) - car_length
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
      return (vmax/2) * (1 - (math.cos(math.pi * (headway - hst) / (hgo - hst))))

  def __str__(self):
    x = self.optimalVelocity(ah, bh, vmax, hst, hgo)
    return f"i_x is {self.distance_travelled % 360}, delta_s is {self.distance_travelled}, OV {x}"

def linkCars(humans):
  for i in range(len(humans)-1):
    humans[i].selectCarInFront(humans[(i+1)])
  humans[-1].selectCarInFront(humans[0])
  return humans

def main(humans):
  while True:
    for car in humans:
      print(f"pos: {round(car.distance_travelled%360)}")
      print(f"v: {round(car.optimalVelocity(ah, bh, vmax, hst, hgo))}")
      car.distance_travelled += car.optimalVelocity(ah, bh, vmax, hst, hgo)
    input()
    print([str(x) for x in humans])

humans = [Human(0), Human(30), Human(80), Human(120), Human(150)]

print(humans[0].getPosition())

main(linkCars(humans))
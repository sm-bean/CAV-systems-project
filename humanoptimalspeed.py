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
    return f"distance travelled is {self.distance_travelled}, optimal velocity {x}"

human1 = Human(50)
human2 = Human(180)
human3 = Human(360)
human1.selectCarInFront(human2)
human2.selectCarInFront(human3)
human3.selectCarInFront(human1)
print(human1)
print(human2)
print(human3)
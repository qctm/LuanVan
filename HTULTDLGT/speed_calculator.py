import math

class SpeedCalculator:
    def __init__(self, m, p):
        self.vehicles = {}
        self.speeds = {}
        self.ppm = m/p

        self.real_vehicle_count = 0
        self.real_speeds = {}
        self.sum_speeds = 0
        self.avg_speed = 0

    def add(self, id, cx, cy, time):
        if id not in self.vehicles:
            coord = [cx, cy, time,0,0,0]
            self.vehicles[id] = coord
        else:
            coord = [self.vehicles[id][0], self.vehicles[id][1], self.vehicles[id][2], cx, cy, time]
            self.vehicles[id] = coord

    def test(self, id):
        if id in self.vehicles:
            print(self.vehicles[id])

    def calculate(self, id, fps):
        if id not in self.speeds.keys() and id in self.vehicles.keys():      
            cx1, cy1, t1, cx2, cy2, t2 = self.vehicles[id]
            if cx2 > 0 and cx2 != cx1:
                d_pixels = math.sqrt(math.pow(cx2-cx1, 2) + math.pow(cy2-cy1, 2))
                d_m = d_pixels * self.ppm
                # Thoi gian
                t = t2 - t1
                # Van toc
                # pixel tren giay
                v = ((d_m / t) * 3.6)*(30/fps)
                self.sum_speeds +=v
                self.speeds[id] = v
                self.avg_speed = round(self.sum_speeds / len(self.speeds), 2)
                self.vehicles.pop(id)
                # print("Vehicle ID: %3d --- speed: %2.1f km/h" %(id, self.speeds[id]))
        if id not in self.vehicles.keys():
            return False
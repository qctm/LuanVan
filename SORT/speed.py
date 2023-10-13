import math

class SpeedCal:
    def __init__(self, p, m):
        self.vehicle_dict = {}  # id : vt1, vt2
        self.speed_dict = {}
        self.avg_speed = 0
        self.sum_speed = 0
        self.ppm = m/p
    
    def add(self, id, cx, cy, time):
        if id not in self.vehicle_dict:
            coord = [cx, cy, time,0,0,0]
            self.vehicle_dict[id] = coord
        else:
            coord = [self.vehicle_dict[id][0], self.vehicle_dict[id][1], self.vehicle_dict[id][2], cx, cy, time]
            self.vehicle_dict[id] = coord
    
    def update(self, id, fps):
        # tinh van toc
        # Khoang cach
        if id not in self.speed_dict.keys():      
            # print(self.vehicle_dict[id])
            cx1, cy1, t1, cx2, cy2, t2 = self.vehicle_dict[id]
            if cx2 > 0 and cx2 != cx1:
                d_pixels = math.sqrt(math.pow(cx2-cx1, 2) + math.pow(cy2-cy1, 2))
                d_m = d_pixels * self.ppm
                # Thoi gian
                t = t2 - t1
                # Van toc
                            # pixel tren giay
                v = ((d_m / t) * 3.6)*(30/fps)
                self.sum_speed +=v
                self.speed_dict[id] = v
                self.avg_speed = self.sum_speed / len(self.speed_dict)
                self.vehicle_dict.pop(id)
                self.print_vehicle_speed(id)

    def print_vehicle_speed(self, id):
        print("Vehicle ID: %3d --- speed: %2.1f km/h" %(id, self.speed_dict[id]))
import math

class SpeedCal:
    def __init__(self):
        self.xe_dict = {}
        self.done = []
        self.sum_vt = 0
    
    def add(self, id, cx1, cy1, time1):
        if id not in self.xe_dict:
            self.xe_dict[id] = (cx1, cy1, time1)
    
    def calcu(self, id, cx2, cy2, time2, fps):
        # Khoang cach
        cx1, cy1, time1 = self.xe_dict[id]
        d_pixels = math.sqrt(math.pow(cx2-cx1, 2) + math.pow(cy2-cy1, 2))
        d_m = d_pixels * 0.06
        # Thoi gian
        time = time2 - time1
            
        # Van toc
                # pixel tren giay
        vantoc = ((d_m / time) * 3.6)*(30/fps)
        self.sum_vt += vantoc
        self.done.append(id)
        avg_vantoc = self.sum_vt / len(self.done)        
        return avg_vantoc
import math

class Tracker_Centroid:
    def __init__(self):
        self.centroid_dict = {}
        self.id_count = 1
    
    def tracking(self, obj_rect):
        objbb_id = [] # ds = obj bouding box + obj ID
        threshold_distance = 30
        # Lay trong tam doi tuong moi
        for rect in obj_rect:
            x, y, w, h = rect   #toa do x, y goc phai tren; w,h rong cao
            cx = (x + (x+w)) // 2
            cy = (y + (y+w)) // 2
            #kiem tra doi tuong moi
            obj_like_obj = False
            for id, ct in self.centroid_dict.items():
                # distance = math.sqrt(math.pow(cx - ct[0],2) + (math.pow(cy - ct[1], 2)))
                # Dung: math.hypot
                distance = math.hypot(cx - ct[0], cy - ct[1])
                if distance < threshold_distance:   # doi tuong da co
                    distance = int(distance)
                    self.centroid_dict[id] = (cx, cy)
                    objbb_id.append([x, y, w, h, id])
                    obj_like_obj = True
                    break
            # doi tuong moi
            if obj_like_obj is False:
                self.centroid_dict[self.id_count] = (cx, cy)
                objbb_id.append([x, y, w, h, self.id_count])
                self.id_count+=1
        # tra ve du liu moi:
        new_centroid_dict = {}
        for objbbid in objbb_id:
            x, y, w, h, id = objbbid
            centroid = self.centroid_dict[id]
            new_centroid_dict[id] = centroid
        
        self.centroid_dict = new_centroid_dict.copy()
        return objbb_id
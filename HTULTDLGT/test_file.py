import torch
import numpy as np
import cv2
def get_bbox_in_roi(tensor, roi):
    t = torch.arange(6).reshape(1, 6)
    new_tensor = ''
    for row in tensor:
        x1, y1, x2, y2 = row[0], row[1], row[2], row[3]
        cx = (int(x1) + int(x2)) / 2
        cy = (int(y1) + int(y2)) / 2
        if cv2.pointPolygonTest(np.array(roi, np.int32), (cx, cy), False) >= 0:
            new_row = torch.tensor(row)
            new_tensor = torch.cat((t, new_row.reshape(1, 6)), 0)
    new_tensor = torch.cat((new_tensor[:0],new_tensor[0+1:]))
    return new_tensor

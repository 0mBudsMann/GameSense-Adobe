def get_center_of_box(box):
    x1, x2, y1, y2 = box
    center_x = int((x1 + x2)/2)
    center_y = int((y1 + y2) / 2)

    return center_x, center_y

def measure_distance(p1, p2):
    return ((p1[2]-p2[2])**2 + (p1[3]-p2[3])**2)**0.5

def get_foot_position(bbox):
    x1,y1,x2,y2 = bbox
    return int((x1+x2)/2),int(y2)

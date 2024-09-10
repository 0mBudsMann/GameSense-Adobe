import json

SINGLES_WIDTH = 5.18
DOUBLES_WIDTH = 6.1
VERTICAL_LENGTH = 13.4

with open('result/court_and_net/courts/court_kp/coordinates.json', 'r') as f:
    data = json.load(f)

court_coord = data["court_info"]
def get_center_of_box(box):
    x1, x2, y1, y2 = box
    center_x = int((x1 + x2)/2)
    center_y = int((y1 + y2) / 2)

    return center_x, center_y

def measure_distance(p1, p2):
    return (((p1[2]-p2[2])**2)*(SINGLES_WIDTH / (court_coord[5][0] - court_coord[0][0])) + ((p1[3]-p2[3])**2)*(VERTICAL_LENGTH / (court_coord[5][1] - court_coord[0][1])))**0.5

def get_foot_position(bbox):
    x1,y1,x2,y2 = bbox
    return int((x1+x2)/2),int(y2)

def get_bbox_width(bbox):
    x1, x2, _, _ = bbox
    return x2 - x1

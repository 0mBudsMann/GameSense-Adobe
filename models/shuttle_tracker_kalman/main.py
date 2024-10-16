import pandas as pd
from numpy.linalg import inv
import numpy as np
import math
import cv2
import torch

from matplotlib import pyplot as plt

import torch
from ultralytics import YOLO

model = YOLO('/content/drive/MyDrive/best.pt')  # Ensure you have the correct model file

# Ensure to use the GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

def draw_prediction(img: np.ndarray,
                    class_name: str,
                    df: pd.core.series.Series,
                    color: tuple = (255, 0, 0)):
    '''
    Function to draw prediction around the bounding box identified by the YOLO
    The Function also displays the confidence score top of the bounding box
    '''

    cv2.rectangle(img, (int(df.xmin), int(df.ymin)),
                  (int(df.xmax), int(df.ymax)), color, 2)
    cv2.putText(img, class_name + " " + str(round(df.confidence, 2)),
                (int(df.xmin) - 10, int(df.ymin) - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return img

def convert_video_to_frame(path: str):
    '''
    The function take input as video file and returns a list of images for every video
    '''
    i=0
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    img = []

    while cap.isOpened() and len(img)<=300:
        i+=1
        print(i)
        ret, frame = cap.read()
        if ret == True:
            img.append(frame)
        else:
            break

    cap.release()
    return img, fps
# Converting Video to image frame by frame for a single and multiple ball

img_multi, fps_multi = convert_video_to_frame('/content/drive/MyDrive/oop.mp4')
#img_sin,# fps_sin = convert_video_to_frame('/content/drive/MyDrive/ass.mp4')
results_multi = model(img_multi)
print(results_multi)
# Assuming the list contains results in a format compatible with pandas conversion
df_multi_list = []
for res in results_multi:
    boxes = res.boxes.xyxy.cpu().numpy()  # Get the bounding boxes
    class_ids = res.boxes.cls.cpu().int().numpy()  # Get the class IDs
    scores = res.boxes.conf.cpu().numpy()  # Get the confidence scores

    # Create a DataFrame from the detection results
    df = pd.DataFrame({'xmin': boxes[:, 0], 'ymin': boxes[:, 1], 'xmax': boxes[:, 2], 'ymax': boxes[:, 3], 'class_id': class_ids, 'confidence': scores})
    df_multi_list.append(df)

# Concatenate the DataFrames into a single DataFrame
df_multi = pd.concat(df_multi_list, ignore_index=True)

class KalmanFilter():
    def __init__(self,
                 xinit: int = 0,
                 yinit: int = 0,
                 fps: int = 30,
                 std_a: float = 0.001,
                 std_x: float = 0.0045,
                 std_y: float = 0.01,
                 cov: float = 100000) -> None:

        # State Matrix
        self.S = np.array([xinit, 0, 0, yinit, 0, 0])
        self.dt = 1 / fps

        # State Transition Model
        # Here, we assume that the model follow Newtonian Kinematics
        self.F = np.array([[1, self.dt, 0.5 * (self.dt * self.dt), 0, 0, 0],
                           [0, 1, self.dt, 0, 0, 0], [0, 0, 1, 0, 0, 0],
                           [0, 0, 0, 1, self.dt, 0.5 * self.dt * self.dt],
                           [0, 0, 0, 0, 1, self.dt], [0, 0, 0, 0, 0, 1]])

        self.std_a = std_a

        # Process Noise
        self.Q = np.array([
            [
                0.25 * self.dt * self.dt * self.dt * self.dt, 0.5 * self.dt *
                self.dt * self.dt, 0.5 * self.dt * self.dt, 0, 0, 0
            ],
            [
                0.5 * self.dt * self.dt * self.dt, self.dt * self.dt, self.dt,
                0, 0, 0
            ], [0.5 * self.dt * self.dt, self.dt, 1, 0, 0, 0],
            [
                0, 0, 0, 0.25 * self.dt * self.dt * self.dt * self.dt,
                0.5 * self.dt * self.dt * self.dt, 0.5 * self.dt * self.dt
            ],
            [
                0, 0, 0, 0.5 * self.dt * self.dt * self.dt, self.dt * self.dt,
                self.dt
            ], [0, 0, 0, 0.5 * self.dt * self.dt, self.dt, 1]
        ]) * self.std_a * self.std_a

        self.std_x = std_x
        self.std_y = std_y

        # Measurement Noise
        self.R = np.array([[self.std_x * self.std_x, 0],
                           [0, self.std_y * self.std_y]])

        self.cov = cov

        # Estimate Uncertainity
        self.P = np.array([[self.cov, 0, 0, 0, 0, 0],
                           [0, self.cov, 0, 0, 0, 0],
                           [0, 0, self.cov, 0, 0, 0],
                           [0, 0, 0, self.cov, 0, 0],
                           [0, 0, 0, 0, self.cov, 0],
                           [0, 0, 0, 0, 0, self.cov]])

        # Observation Matrix
        # Here, we are observing X & Y (0th index and 3rd Index)
        self.H = np.array([[1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0]])

        self.I = np.array([[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0],
                           [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0],
                           [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]])

        # Predicting the next state and estimate uncertainity
        self.S_pred = None
        self.P_pred = None

        # Kalman Gain
        self.K = None

        # Storing all the State, Kalman Gain and Estimate Uncertainity
        self.S_hist = [self.S]
        self.K_hist = []
        self.P_hist = [self.P]

    def pred_new_state(self):
        self.S_pred = self.F.dot(self.S)

    def pred_next_uncertainity(self):
        self.P_pred = self.F.dot(self.P).dot(self.F.T) + self.Q

    def get_Kalman_gain(self):
        self.K = self.P_pred.dot(self.H.T).dot(
            inv(self.H.dot(self.P_pred).dot(self.H.T) + self.R))
        self.K_hist.append(self.K)

    def state_correction(self, z):
        if z == [None, None]:
            self.S = self.S_pred
        else:
            self.S = self.S_pred + +self.K.dot(z - self.H.dot(self.S_pred))

        self.S_hist.append(self.S)

    def uncertainity_correction(self, z):
        if z != [None, None]:
            self.l1 = self.I - self.K.dot(self.H)
            self.P = self.l1.dot(self.P_pred).dot(self.l1.T) + self.K.dot(
                self.R).dot(self.K.T)
        self.P_hist.append(self.P)



filter_multi = [
    KalmanFilter(fps=fps_multi, xinit=60, yinit=150,
                 std_x=0.000025, std_y=0.0001),

]

def cost_fun(a, b):
    '''
    Cost function for filter Assignment
    Uses euclidean distance for choosing the filter
    '''

    sm = 0
    for i in range(len(a)):
        sm += (a[i] - b[i])**2
    return sm

ind = 0
out = cv2.VideoWriter('multiple_balls_kalman.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps_multi,
                      (img_multi[0].shape[1], img_multi[0].shape[0]))

assig = []
for _, row in df_multi.iterrows():
    coord = [(row['xmin'] + row['xmax']) / 2,
             (row['ymin'] + row['ymax']) / 2]

    # Determine which filter to use
    cost0 = cost_fun([filter_multi[0].S_hist[-1][0], filter_multi[0].S_hist[-1][3]], coord)


    x_cen, y_cen = coord[0], coord[1]
    assig.append(0)


    # Update the Kalman Filters
    for i in range(1):
        filter_multi[i].pred_new_state()
        filter_multi[i].pred_next_uncertainity()
        filter_multi[i].get_Kalman_gain()
        filter_multi[i].state_correction([x_cen, y_cen] if assig[-1] == i else [None, None])
        filter_multi[i].uncertainity_correction([x_cen, y_cen] if assig[-1] == i else [None, None])

for i in range(len(img_multi)):
    tmp_img = img_multi[i].copy()

    # Draw the predicted positions of the two balls
    for j, filter in enumerate(filter_multi):
        if(filter is None or len(filter.S_hist)<=i):
           continue
        color = (255, 0, 0) if j == 0 else (0, 0, 255)
        predicted_pos = (int(filter.S_hist[i][0]), int(filter.S_hist[i][3]))
        cv2.circle(tmp_img, predicted_pos, radius=1, color=color, thickness=3)

    # Get detections for the current frame
    current_detections = df_multi_list[i]

    for _, row in current_detections.iterrows():
        # Draw bounding box for all detected objects
        if row['class_id'] == 0:  # Assuming 0 is the class ID for 'sports ball'
            # Determine which filter this detection is closer to
            coord = [(row['xmin'] + row['xmax']) / 2, (row['ymin'] + row['ymax']) / 2]
            if filter_multi[0] is not None and len(filter_multi[0].S_hist) > i:
              cost0 = cost_fun([filter_multi[0].S_hist[i][0], filter_multi[0].S_hist[i][3]], coord)
            if filter_multi[0] is not None:

              color = (255, 0, 0)  # Red for objects closer to filter 0
              label = 'Ball 1'


            tmp_img = draw_prediction(tmp_img, label, row, color=color)

    out.write(tmp_img)

out.release()

from IPython.display import Video
Video("multiple_balls_kalman.mp4", embed=True)


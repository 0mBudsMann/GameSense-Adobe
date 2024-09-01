from ultralytics import YOLO

# model = YOLO('weights/only_player/best.pt')
# pose yolo model
model = YOLO('yolov8m-pose')
result = model.predict('../../utils/footages/12sec.mp4', save=True)

print(result)

print("boxes: ")

for box in result[0].boxes:
    print(box)

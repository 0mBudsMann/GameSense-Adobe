from ultralytics import YOLO

# model = YOLO('weights/only_player/best.pt')
# pose yolo model
model = YOLO('../../trackers/tests/yolov8m.pt')
result = model.predict('../../utils/footages/doubles.mp4', save=True)

print(result)

print("boxes: ")

for box in result[0].boxes:
    print(box)

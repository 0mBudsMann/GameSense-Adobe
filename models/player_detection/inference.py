from ultralytics import YOLO

model = YOLO('weights/best.pt')

result = model.predict('../../utils/footages/short.mp4', save=True)

print(result)

print("boxes: ")

for box in result[0].boxes:
    print(box)

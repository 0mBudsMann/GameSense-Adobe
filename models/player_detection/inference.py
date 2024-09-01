from ultralytics import YOLO

model = YOLO('weights/shuttle_player_racquet/last.pt')

result = model.predict('../../utils/footages/12sec.mp4', save=True)

print(result)

print("boxes: ")

for box in result[0].boxes:
    print(box)

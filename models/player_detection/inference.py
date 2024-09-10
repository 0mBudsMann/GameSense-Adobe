from ultralytics import YOLO

# model = YOLO('weights/only_player/best.pt')
# pose yolo model
model = YOLO('../player_and_shuttle_combined/weights/best.pt')
result = model.predict('../../utils/footages/10sec.mp4', save=True)

print(result)

print("boxes: ")

for box in result[0].boxes:
    print(box)

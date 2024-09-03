from roboflow import Roboflow
import shutil

rf = Roboflow(api_key="PUPX5QV9wrs9aSPZAS4J")
project = rf.workspace("mathieu-cartron").project("shuttlecock-cqzy3")
version = project.version(1)
dataset = version.download("yolov8")

shutil.move("Shuttlecock-1/train", "Shuttlecock-1/Shuttlecock-1/train")
shutil.move("Shuttlecock-1/valid", "Shuttlecock-1/Shuttlecock-1/valid")
shutil.move("Shuttlecock-1/test", "Shuttlecock-1/Shuttlecock-1/test")
import roboflow

# Initialize Roboflow API
rf = roboflow.Roboflow(api_key="5keK78Jd2vJ9EB7lacGU")
project = rf.workspace().project("indian-emergency-vehicles-dataset")

# Specify version and deploy
version = project.version(1)
version.deploy(
    "yolov8",
    r"D:\Desktop\PROJs\Multiple Emergency Vehicles Detection and Traffic\SwiftPass-AI-Powered-Emergency-Traffic-Control\Model\YOLO-Trained-Model\content\runs\detect\train\weights",
    "best.pt"
)

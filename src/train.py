from ultralytics import YOLO

# Load a model
model = YOLO('models/yolov8n.pt')
results = model.train(data='data/project1/edited/a.yaml', epochs=10, imgsz=640, device='cpu')
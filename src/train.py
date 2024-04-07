from ultralytics import YOLO

# Load a model
def tr(modelPath):
    model = YOLO(modelPath)
    results = model.train(data='data/project1/edited/a.yaml', epochs=10, imgsz=640, device='cpu')
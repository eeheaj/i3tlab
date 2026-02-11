from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # lightweight model

def detect_objects(image_path, target_classes=None, conf=0.4):
    results = model(image_path, conf=conf)

    detected = set()
    detections = []

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            confidence = float(box.conf[0])

            if target_classes is None or label in target_classes:
                detected.add(label)
                detections.append({
                    "label": label,
                    "confidence": confidence,
                    "bbox": box.xyxy[0].tolist()
                })

    return detected, detections

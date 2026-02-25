YOLO_CLASS_MAP = {
    "coffee maker": "coffee machine",
    "coffee mug": "cup",
    "mug": "cup",
    "water bottle": "bottle",
    "paper filter": "filter",
    "coffee grounds": "coffee"
}

def map_to_yolo_classes(objects):
    mapped = []
    unsupported = []

    for obj in objects:
        if obj in YOLO_CLASS_MAP:
            mapped.append(YOLO_CLASS_MAP[obj])
        else:
            unsupported.append(obj)

    return list(set(mapped)), unsupported

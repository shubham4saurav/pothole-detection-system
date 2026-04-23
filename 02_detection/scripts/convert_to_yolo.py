import os
import xml.etree.ElementTree as ET
from PIL import Image

# Paths
dataset_path = "/Users/shubham/Desktop/projects/pothole detection system/dataset"
IMAGE_DIR = os.path.join(dataset_path, "potholes/images")
ANNOTATION_DIR = os.path.join(dataset_path, "potholes/annotations")
OUTPUT_LABEL_DIR = os.path.join(dataset_path, "potholes/labels")

os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)

def convert_box(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]

    x_center = (box[0] + box[2]) / 2.0
    y_center = (box[1] + box[3]) / 2.0

    width = box[2] - box[0]
    height = box[3] - box[1]

    x_center *= dw
    y_center *= dh
    width *= dw
    height *= dh

    return (x_center, y_center, width, height)

for xml_file in os.listdir(ANNOTATION_DIR):
    if not xml_file.endswith(".xml"):
        continue

    tree = ET.parse(os.path.join(ANNOTATION_DIR, xml_file))
    root = tree.getroot()

    image_file = root.find("filename").text
    image_path = os.path.join(IMAGE_DIR, image_file)

    # Get image size
    with Image.open(image_path) as img:
        w, h = img.size

    label_file = xml_file.replace(".xml", ".txt")
    label_path = os.path.join(OUTPUT_LABEL_DIR, label_file)

    with open(label_path, "w") as f:
        for obj in root.findall("object"):
            cls = obj.find("name").text

            if cls != "pothole":
                continue

            xmlbox = obj.find("bndbox")
            b = (
                float(xmlbox.find("xmin").text),
                float(xmlbox.find("ymin").text),
                float(xmlbox.find("xmax").text),
                float(xmlbox.find("ymax").text),
            )

            bb = convert_box((w, h), b)

            # class_id = 0 (only pothole)
            f.write(f"0 {bb[0]} {bb[1]} {bb[2]} {bb[3]}\n")

print("Conversion completed!")
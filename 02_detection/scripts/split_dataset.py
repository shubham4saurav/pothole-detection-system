import os
import random
import shutil

dataset_path = "/Users/shubham/Desktop/projects/pothole detection system/dataset"
IMAGE_DIR = os.path.join(dataset_path, "potholes/images")
LABEL_DIR = os.path.join(dataset_path, "potholes/labels")

OUTPUT_DIR = os.path.join(dataset_path, "potholes")

train_ratio = 0.8

images = [f for f in os.listdir(IMAGE_DIR) if f.endswith(".png")]

random.shuffle(images)

split_index = int(len(images) * train_ratio)

train_images = images[:split_index]
val_images = images[split_index:]
print(f"Total images: {len(images)}")
print(f"Training images: {len(train_images)}")
def copy_files(image_list, split):
    for img in image_list:
        label = img.replace(".png", ".txt")

        src_img = os.path.join(IMAGE_DIR, img)
        src_lbl = os.path.join(LABEL_DIR, label)

        dst_img = os.path.join(OUTPUT_DIR, split, "images", img)
        dst_lbl = os.path.join(OUTPUT_DIR, split, "labels", label)

        os.makedirs(os.path.dirname(dst_img), exist_ok=True)
        os.makedirs(os.path.dirname(dst_lbl), exist_ok=True)

        shutil.copy(src_img, dst_img)
        if os.path.exists(src_lbl):
            shutil.copy(src_lbl, dst_lbl)

copy_files(train_images, "train")
copy_files(val_images, "val")

print("Dataset split completed!")
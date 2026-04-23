import cv2

def is_blurry(image_path, threshold=100):
    img = cv2.imread(str(image_path), 0)
    variance = cv2.Laplacian(img, cv2.CV_64F).var()
    return variance < threshold

def is_too_dark(image_path, threshold=40):
    img = cv2.imread(str(image_path), 0)
    return img.mean() < threshold

def is_valid_size(bbox, min_area=500):
    x1, y1, x2, y2 = bbox
    area = (x2 - x1) * (y2 - y1)
    return area > min_area
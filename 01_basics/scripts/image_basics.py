import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("../images/test.jpg")

if image is None:  
    print("Could not read the image.")
    exit()

print("Type of the image:", type(image))
print("Shape of the image:", image.shape)

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

print("Pixel value at (100, 100):", image[100, 100])

image[100,100] = [255,0,0]

cv2.rectangle(image, (50, 50), (150, 150), (0, 255, 0), 3)

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Modified Image")
plt.axis('off')
plt.show()

edges = cv2.Canny(image, 50, 250)
plt.imshow(edges, cmap='gray')
plt.title("Canny Edges")
plt.axis('off')
plt.show()
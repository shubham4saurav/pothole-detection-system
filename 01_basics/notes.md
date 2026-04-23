## What is an Image?
- Grid of pixels
- Each pixel has values (RGB)

## Image Representation
- Stored as NumPy array
- Shape = (height, width, channels)

## Key Learnings
- Image is just numbers
- We can modify pixels directly

## Grayscale
- Removes color, keeps intensity

## Edge Detection
- Detects boundaries
- Useful for potholes

## My Understanding
- AI uses fixed sized images like 640x640. it is important to resize before feeding in any algo.
## Edge Detection (Very Simple)

- Think of an image like a map of brightness values.
- An edge is where brightness changes suddenly (light to dark or dark to light).
- Canny checks every area and keeps only these sharp-change boundaries.

In `cv2.Canny(image, 100, 200)`:
- `100` = lower limit
- `200` = higher limit
- Very clear boundaries are kept.
- Very weak boundaries are removed.
- Medium ones are kept only if they touch a clear boundary.

So final output is mostly object outlines and road cracks/pothole borders, not full image details.

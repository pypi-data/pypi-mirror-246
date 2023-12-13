import os

os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2, 40).__str__()
import cv2
import matplotlib.pyplot as plt
import numpy as np
import skimage.measure
import skimage.morphology
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_triangle, try_all_threshold


def show_image(mat: np.ndarray) -> None:
    plt.imshow(mat)
    plt.show()


mask = cv2.imread("mask_1.tif", cv2.IMREAD_GRAYSCALE)
mask = mask > 0
chunk = mask[40000:60000, :]
opening = skimage.morphology.binary_opening(chunk)
for i in range(4):
    opening = skimage.morphology.binary_opening(opening)

connected_components = skimage.measure.label(opening, connectivity=2)

with open("src/hmsm/data/lut.npy", "rb") as f:
    lut = np.load(f)

bg = connected_components % 255
bg = bg.astype(np.uint8)

clr_image = cv2.LUT(cv2.merge((bg, bg, bg)), lut)

# Calculate threshold on partial image to ease memory constrains
img_gray = io.imread("data/5060708_chunk.tif", as_gray=True)
threshold = threshold_triangle(img_gray)

# Read grayscale image using opencv (because skimage will run out of memory) and binarize it
img_gray = cv2.imread("data/5060708_7_cropped.tif", cv2.IMREAD_GRAYSCALE)
binary = img_gray > (threshold * 255)
del img_gray

# Read input image

img = io.imread("data/5060708_chunk.tif")

# Take all pixels that are binarized to 0 and convert to pixel list
pixels = img.reshape((-1, 3))
pixels = img[binary == False].reshape((-1, 3))
pixels = np.float32(pixels)

# Cluster into two clusters based on color

stop_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.2)
k = 3
_, labels, (centers) = cv2.kmeans(
    pixels, k, None, stop_criteria, 10, cv2.KMEANS_RANDOM_CENTERS
)
del pixels


arr = np.array([[1, 4, 5, 0], [0, 2, 4, 1], [2, 4, 7, 1]])
colsums = np.sum(arr, axis=0)
threshold = 5
accepted_cols = np.where(colsums > threshold)
start_idx, end_idx = accepted_cols[0][0], accepted_cols[0][-1]

# Create "masks"

centers = np.uint8(centers)
labels = labels.flatten()

classified_pixels = img.reshape((-1, 3))
classified_pixels[labels == 0] = [255, 0, 0]
classified_pixels[labels == 1] = [0, 255, 0]
classified_pixels[labels == 2] = [0, 0, 255]
img = classified_pixels.reshape(img.shape)

cv2.imwrite("segmented.tif", img)

# misc

seg_img = centers[labels.flatten()]

display_image = img.copy()

display_image[binary == False] = seg_img.reshape(img[binary == False].shape)

plt.imshow(display_image)
plt.show()


fig, ax = try_all_threshold(img_gray, figsize=(10, 8), verbose=False)
plt.show()

img = cv2.imread("data/5060708_chunk.tif")

average = img.mean(axis=0).mean(axis=0)

img.shape

pixels = list()


def kosten_dieses_meetings(n_wma: int, n_hiwi: int, dauer: float):
    return ((n_wma * 36) + (n_hiwi * 16)) * dauer

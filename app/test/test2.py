import cv2
from matplotlib import pyplot as plt
from image_processing import main_process
from text_detection import main_detection
from other_function import plot_images
from extract_info import extract_info

# Đường dẫn đến ảnh cần phân tích
image_path = './bill.jpg'
img = cv2.imread(image_path)
text_result = plot_images(img)
print(extract_info(text_result)) 
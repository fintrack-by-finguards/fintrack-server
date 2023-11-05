import cv2
from matplotlib import pyplot as plt
from app.text_detection.image_processing import main_process
from text_detection import main_detection
from app.text_detection.other_function import plot_images
from app.text_detection.extract_info import extract_info

# Đường dẫn đến ảnh cần phân tích
image_path = './bill.jpg'
text_result = plot_images(image_path)
print(extract_info(text_result)) 
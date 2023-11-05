import cv2
from matplotlib import pyplot as plt
from app.text_detection.image_processing import main_process
from text_detection import main_detection

def plot_images(image_path): 
    processed_image = main_process(image_path)
    text_result, detection_image = main_detection(processed_image)

    print(text_result)

    original_image = cv2.imread(image_path)

    # Chuyển đổi ảnh từ BGR sang RGB
    original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    detection_image_rgb = cv2.cvtColor(detection_image, cv2.COLOR_BGR2RGB)

    # Thiết lập plot
    plt.figure(figsize=(15, 5))

    # Hiển thị ảnh gốc
    plt.subplot(1, 3, 1) # 1 hàng, 3 cột, vị trí thứ nhất
    plt.imshow(original_image_rgb)
    plt.title('Original Image')
    plt.axis('off')  # Tắt trục tọa độ

    # Hiển thị ảnh đã chỉnh sửa
    plt.subplot(1, 3, 2) # 1 hàng, 3 cột, vị trí thứ hai
    plt.imshow(processed_image, cmap='gray')
    plt.title('Processed Image')
    plt.axis('off')  # Tắt trục tọa độ

    # Hiển thị ảnh đã chỉnh sửa
    plt.subplot(1, 3, 3) # 1 hàng, 3 cột, vị trí thứ hai
    plt.imshow(detection_image_rgb)
    plt.title('Text Detection Image')
    plt.axis('off')  # Tắt trục tọa độ

    # Hiển thị cửa sổ chứa hai ảnh
    # plt.show()
    return text_result

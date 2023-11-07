import numpy as np
import cv2
import pytesseract
from pytesseract import Output

# Tính góc nghiêng trung bình của ảnh
def get_skew_angle(cv_image) -> float:
    # Chuyển đổi sang grayscale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    # Áp dụng ngưỡng để tăng độ tương phản giữa hóa đơn và nền
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Phát hiện các cạnh trong ảnh
    edges = cv2.Canny(thresh, 50, 150, apertureSize=3)
    # Sử dụng Hough Transform để phát hiện đường thẳng trong ảnh
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10) # Adjusted minLineLength

    # Lọc các đường thẳng dựa trên góc để tính góc nghiêng
    angles = []
    if lines is not None:  # Check if any line was detected
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * (180 / np.pi)
            # Exclude angles too far from horizontal & vertical
            if -45 < angle < 45 or 135 < angle < 225:
                angles.append(angle)
    
    # If no angle meets the criteria above, no skew correction is needed
    if not angles:
        return 0

    # Calculate the average angle of the lines
    median_angle = np.median(angles)
    return median_angle

# Xoay ảnh theo góc nghiêng
def deskew(cv_image):
    angle = get_skew_angle(cv_image)
    if angle != 0:  # Perform deskew operation only if an angle was detected
        # Xác định trung tâm ảnh và góc xoay
        (h, w) = cv_image.shape[:2]
        center = (w // 2, h // 2)
        # Thực hiện xoay ảnh
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(cv_image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated
    else:
        return cv_image  #
    
def main_process(image):
    # Đọc ảnh sử dụng OpenCV
    # image = cv2.imread(image_path)
    # if image is None:
    #     print(f"Error: Unable to load image at {image_path}")
    #     exit()

    # Chuyển đổi sang grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Áp dụng GaussianBlur để giảm nhiễu
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Sử dụng Tesseract để phát hiện văn bản từ ảnh xám
    custom_config = r'--oem 3 --psm 6'
    details = pytesseract.image_to_data(blurred, output_type=Output.DICT, config=custom_config, lang='vie')

    # Khởi tạo tọa độ để tạo hình chữ nhật lớn nhất chứa toàn bộ văn bản
    x_min = np.min([details['left'][i] for i in range(len(details['text'])) if int(details['conf'][i]) > 0])
    y_min = np.min([details['top'][i] for i in range(len(details['text'])) if int(details['conf'][i]) > 0])
    x_max = np.max([details['left'][i] + details['width'][i] for i in range(len(details['text'])) if int(details['conf'][i]) > 0])
    y_max = np.max([details['top'][i] + details['height'][i] for i in range(len(details['text'])) if int(details['conf'][i]) > 0])

    # Xác định kích thước của hình ảnh
    height, width = image.shape[:2]

    # Thêm padding
    padding = 20  # Padding để tránh mất văn bản khi xoay hoặc xử lý ảnh

    # Điều chỉnh các giá trị tọa độ để không vượt quá biên của hình ảnh gốc
    x_min_pad = max(x_min - padding, 0)
    y_min_pad = max(y_min - padding, 0)
    x_max_pad = min(x_max + padding, width)
    y_max_pad = min(y_max + padding, height)

    # Cắt vùng chứa toàn bộ văn bản cùng với padding
    text_region_padded = image[y_min_pad:y_max_pad, x_min_pad:x_max_pad]
    # Áp dụng deskew cho vùng đã pad
    deskewed_region = deskew(text_region_padded)

    # Chuyển đổi sang grayscale
    final_image = cv2.cvtColor(deskewed_region, cv2.COLOR_BGR2GRAY)

    return final_image

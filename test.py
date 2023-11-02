import cv2
import pytesseract
import requests
import json
from base64 import b64encode
from pytesseract import Output
import numpy as np

def get_skew_angle(cv_image) -> float:
    # Chuyển đổi sang grayscale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    # Phát hiện các cạnh trong ảnh
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # Sử dụng Hough Transform để phát hiện đường thẳng trong ảnh
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=5, maxLineGap=20)

    # Lọc các đường thẳng dựa trên góc để tính góc nghiêng
    angles = []
    if lines is not None:  # Check if any line was detected
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * (180 / np.pi)
            angles.append(angle)
    else:
        return 0  # No angle skew correction if no lines are detected

    # Trả về góc nghiêng trung bình của ảnh
    return np.median(angles)

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
    
def order_points(pts):
    # Sắp xếp các điểm trong theo thứ tự top-left, top-right, bottom-right, bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    # Lấy lại và sắp xếp các điểm
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Tính kích thước mới của ảnh sau khi biến đổi
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # Tạo ma trận biến đổi và thực hiện phép biến đổi góc nhìn
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # Trả về ảnh đã được cắt
    return warped


# Đường dẫn đến ảnh cần phân tích
image_path = './bill3.png'

# API Key của bạn
api_key = 'AIzaSyDizBWdgr2GxKB3g7L3ZiiquLUHTwecRzc'

# Đọc ảnh sử dụng OpenCV
image = cv2.imread(image_path)

deskewed_image = deskew(image)

# Chuyển đổi sang grayscale
gray = cv2.cvtColor(deskewed_image, cv2.COLOR_BGR2GRAY)
# Áp dụng GaussianBlur để giảm nhiễu
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# Phát hiện cạnh bằng Canny
edged = cv2.Canny(blurred, 75, 200)

# Tìm contours
contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

# Duyệt qua các contours tìm thấy
for c in contours:
    # Xấp xỉ contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # Nếu xấp xỉ đủ 4 điểm, giả định rằng chúng ta đã tìm thấy hóa đơn
    if len(approx) == 4:
        screenCnt = approx
        break

try:
    # Hiển thị contour của hóa đơn
    cv2.drawContours(deskewed_image, [screenCnt], -1, (0, 255, 0), 2)
    # Cắt hóa đơn từ ảnh
    warped = four_point_transform(deskewed_image, screenCnt.reshape(4, 2))
    # Chuyển đổi ảnh sang ảnh xám để giảm nhiễu và đơn giản hóa xử lý
    gray_image = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
except NameError:
    # Chuyển đổi ảnh sang ảnh xám để giảm nhiễu và đơn giản hóa xử lý
    gray_image = cv2.cvtColor(deskewed_image, cv2.COLOR_BGR2GRAY)

# Sử dụng Tesseract để phát hiện văn bản từ ảnh xám
custom_config = r'--oem 3 --psm 6'
details = pytesseract.image_to_data(gray_image, output_type=Output.DICT, config=custom_config, lang='eng')

padding = 8  # Thêm một đệm là 10 pixels cho mỗi phía của block text

# Lọc ra những dòng có chứa văn bản
lines = set(details['line_num'])  # Lấy tập hợp các số dòng duy nhất

for line in lines:
    # Lấy các chỉ số của tất cả các phần tử trong dòng hiện tại
    line_elements = [i for i, line_num in enumerate(details['line_num']) if line_num == line]
    if line_elements:  # Nếu dòng có chứa văn bản
        # Lấy tọa độ của block dòng từ phần tử đầu tiên và cuối cùng trong dòng
        x1, y1 = details['left'][line_elements[0]], details['top'][line_elements[0]]
        x2 = details['left'][line_elements[-1]] + details['width'][line_elements[-1]]
        y2 = details['top'][line_elements[-1]] + details['height'][line_elements[-1]]
    
        # Mở rộng block text bằng cách thêm padding
        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(gray_image.shape[1], x2 + padding)
        y2 = min(gray_image.shape[0], y2 + padding)

        # Cắt khối văn bản từ ảnh gốc
        text_block = gray_image[y1:y2, x1:x2]
        
        # Mã hóa khối văn bản thành base64 để gửi tới Google Vision API
        retval, buffer = cv2.imencode('.jpg', text_block)
        base64_text_block = b64encode(buffer).decode()

        # Tạo payload JSON
        json_payload = json.dumps({
            'requests': [{
                'image': {
                    'content': base64_text_block
                },
                'features': [{
                    'type': 'TEXT_DETECTION'
                }]
            }]
        })

        # Định nghĩa endpoint và headers
        url = f'https://vision.googleapis.com/v1/images:annotate?key={api_key}'
        headers = {'Content-Type': 'application/json'}

        # Gửi yêu cầu đến Google Cloud Vision API
        response = requests.post(url, data=json_payload, headers=headers)

        # Xử lý kết quả
        if response.status_code == 200:
            # In ra văn bản được phát hiện
            text_result = response.json().get('responses', [{}])[0].get('fullTextAnnotation', {}).get('text', '')
            print(f'Block Line {line}:')
            print(text_result)
        else:
            print('Error:', response.text)
        
        # Hiển thị khối văn bản
        cv2.imshow(f'Block Line {line}', text_block)
        cv2.waitKey(0)
        
        # Lưu khối văn bản vào một file ảnh, nếu muốn
        # cv2.imwrite(f'block_line_{line}.jpg', text_block)

cv2.destroyAllWindows()

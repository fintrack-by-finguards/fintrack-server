import cv2
import pytesseract
import requests
import json
from base64 import b64encode
from pytesseract import Output
import numpy as np

# API Key của bạn
api_key = 'AIzaSyDizBWdgr2GxKB3g7L3ZiiquLUHTwecRzc'
    
def main_detection(processed_image): 
    # Sử dụng Tesseract để phát hiện văn bản từ ảnh xám
    text_result = []
    custom_config = r'--oem 3 --psm 6'
    details = pytesseract.image_to_data(processed_image, output_type=Output.DICT, config=custom_config, lang='eng')

    padding = 5  # Thêm một đệm là 8 pixels cho mỗi phía của block text

    # Lọc ra những dòng có chứa văn bản
    lines = set(details['line_num'])  # Lấy tập hợp các số dòng duy nhất

    # Tạo một bản sao của ảnh để vẽ viền các block text
    image_with_boxes = processed_image.copy()

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
            x2 = min(processed_image.shape[1], x2 + padding)
            y2 = min(processed_image.shape[0], y2 + padding)

            # Cắt khối văn bản từ ảnh gốc
            text_block = processed_image[y1:y2, x1:x2]

            # Vẽ hình chữ nhật xung quanh block text trên ảnh ban đầu
            cv2.rectangle(image_with_boxes, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            _, buffer = cv2.imencode('.jpg', text_block)
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
                text = response.json().get('responses', [{}])[0].get('fullTextAnnotation', {}).get('text', '')
                text_result.append(text.split("\n"))
            else:
                print('Error:', response.text)
            
    return text_result[1:], image_with_boxes
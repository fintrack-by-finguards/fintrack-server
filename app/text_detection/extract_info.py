# data = [['CÀ PHÊ HOÀNG PHÚC'], ['Đường Số 24 KDC An Khánh, P. An Khánh'], 
#         ['Q. Ninh Kiều - TP. Cần Thơ'], ['ĐT: 0974.300.007 - 0909.191.195'], 
#         ['HÓA ĐƠN BÁN HÀNG'], ['Bàn 06'], ['Ngày: 18/02/2019', 'Số: 021900003'], 
#         ['Thu ngân: Administrator', 'In lúc: 01:41'], ['Giờ vào: 01:41', 'Giờ ra: 01:41'],
#         ['Mặt hàng', 'SL', 'Giá', 'T tiên'], ['Cà phê đá', '1', '10,000', '10,000'], 
#         ['Bún thịt Xào', '1', '15,000', '15,000'], ['Cà phê sữa đá', '1', '12,000', '12,000'], 
#         ['Cơm tấm', '1 17,000', '17,000'], ['Tổng:', '54,000'], ['Cảm ơn Quý khách. Hẹn gặp lại 1']]

address_keywords = ['đường', 'phố', 'ngõ', 'nghách', 'hẻm', 
                    'xã', 'phường', 'thị trấn', 'thành phố', 'tp', 
                    'tỉnh', 'quận', 'huyện', 'khu vực', 'kdc', 
                    'khu đô thị', 'lô', 'lầu', 'tầng', 'nhà', 
                    'biệt thự', 'căn hộ', 'chung cư', 'tòa nhà', 'p.',
                    'q.', 'tp.', 'địa chỉ',
                    'an giang',
                    'bà rịa - vũng tàu', 'ba ria - vung tau', 'baria - vungtau', 'brvt', 'br-vt',
                    'bắc giang', 'bac giang',
                    'bắc kạn', 'bac kan',
                    'bạc liêu', 'bac lieu', 
                    'bắc ninh', 'bac ninh', 
                    'bến tre', 'ben tre', 
                    'bình định', 'binh dinh',
                    'bình dương', 'binh duong',
                    'bình phước', 'binh phuoc',
                    'bình thuận', 'binh thuan', 
                    'cà mau', 'ca mau',
                    'cần thơ', 'can tho',
                    'cao bằng', 'cao bang',
                    'đà nẵng', 'da nang', 
                    'đắk lắk', 'dak lak',
                    'đắk nông', 'dak nong',
                    'điện biên', 'dien bien',
                    'đồng nai', 'dong nai',
                    'đồng tháp', 'dong thap',
                    'gia lai',
                    'hà giang', 'ha giang',
                    'hà nam', 'ha nam',
                    'hà nội', 'ha noi', 'hanoi', 'hn',
                    'hà tĩnh', 'ha tinh',
                    'hải dương', 'hai duong',
                    'hải phòng', 'hai phong', 
                    'hậu giang', 'hau giang',
                    'hòa bình', 'hoa binh', 
                    'hưng yên', 'hung yen',
                    'khánh hòa', 'khanh hoa',
                    'kiên giang', 'kien giang', 
                    'kon tum', 'kontum',
                    'lai châu', 'lai chau',
                    'lâm đồng', 'lam dong', 
                    'lạng sơn', 'lang son',
                    'lào cai', 'lao cai', 
                    'long an',
                    'nam định', 'nam dinh',
                    'nghệ an', 'nghe an',
                    'ninh bình', 'ninh binh',
                    'ninh thuận', 'ninh thuan', 
                    'phú thọ', 'phu tho',
                    'phú yên', 'phu yen',
                    'quảng bình', 'quang binh', 
                    'quảng nam', 'quang nam', 
                    'quảng ngãi', 'quang ngai',
                    'quảng ninh', 'quang ninh',
                    'quảng trị', 'quang tri', 
                    'sóc trăng', 'soc trang',
                    'sơn la', 'son la', 
                    'tây ninh', 'tay ninh',
                    'thái bình', 'thai binh', 
                    'thái nguyên', 'thai nguyen',
                    'thanh hóa', 'thanh hoa',
                    'thừa thiên huế', 'thua thien hue', 'tth',
                    'tiền giang', 'tien giang', 
                    'tp hồ chí minh', 'tp ho chi minh', 'tphcm', 'hcm',
                    'trà vinh', 'tra vinh',
                    'tuyên quang', 'tuyen quang', 
                    'vĩnh long', 'vinh long',
                    'vĩnh phúc', 'vinh phuc',
                    'yên bái', 'yen bai',]

header_keywords = {
    'ghi_chu': ['ghi chú', 'mô tả', 'tên món', 'item', 'mặt hàng', 'description'],
    'so_luong': ['sl', 'số lượng', 'qty', 'quantity'],
    'gia': ['giá', 'đơn giá', 'price', 'unit price'],
    'tong': ['tổng', 'thành tiền', 't tiền', 'total', 'subtotal']
}

total_payment_keywords = ['tổng cộng', 'tổng tiền', 'tổng']

import re
from datetime import datetime

def extract_info(data):
    try:
        ten_quan = ""
        dia_chi = ""
        ngay = ""
        gio = ""
        tong_tien = 0
        num_header = 0
        menu_items = []
        header_index = {}
        header_line = -1
        date_patterns = {
            re.compile(r'\b\d{2}/\d{2}/\d{4}\b'): "%d/%m/%Y",
            re.compile(r'\b\d{2}-\d{2}-\d{4}\b'): "%d-%m-%Y",
            re.compile(r'\b\d{2}\.\d{2}\.\d{4}\b'): "%d.%m.%Y",
            re.compile(r'\b\d{4}-\d{2}-\d{2}\b'): "%Y-%m-%d"
        }
        total_payment_index = -1

        time_pattern = re.compile(r'\b\d{2}:\d{2}\b')
        # 2023-06-28
        price_patterns = {
            re.compile(r'\d+.\d+'),
            re.compile(r'\d+,\d+')
        }

        for idx, block in enumerate(data):
            block_text = ' '.join(block)  # Nối các phần tử trong block
            block_text_lower = block_text.lower()

            # Xác định tên quán dựa trên một số tiêu chí nào đó
            if len(block) == 1 and 10 < len(block_text) < 30 and ten_quan == "":
                ten_quan = block_text

            # Tìm kiếm trong mỗi chuỗi của block
            for text in block:
                text_lower = text.lower()
                if any(keyword in text_lower for keyword in address_keywords):
                    # Tìm từ khóa và loại bỏ "Địa chỉ" nếu nó xuất hiện
                    address_line = re.sub(r'^.*địa chỉ:\s*', '', text, flags=re.IGNORECASE).strip()
                    # Bây giờ address_line chứa chuỗi có từ khóa địa chỉ mà không có "Địa chỉ"
                    
                    # Kiểm tra xem chuỗi sau khi đã loại bỏ "Địa chỉ" có hợp lệ hay không
                    if address_line and not address_line.isspace():
                        if(dia_chi == "") :
                            dia_chi = address_line 
                        else:
                            dia_chi = dia_chi + " " + address_line
                        break  # Chỉ lấy phần tử đầu tiên thoả mãn điều kiện

            
            # Tìm kiếm và trích xuất ngày
            for pattern, date_format in date_patterns.items():
                match = pattern.search(block_text_lower)
                if match:
                    # Chuyển đổi ngày về định dạng dd/mm/yyyy
                    date_obj = datetime.strptime(match.group(), date_format)
                    ngay = date_obj.strftime("%d/%m/%Y")
                    break 

            # Tìm kiếm giờ theo biểu thức chính quy đã định nghĩa
            time_match = time_pattern.search(block_text_lower)
            if time_match:
                gio = time_match.group()  # Lưu giá trị giờ

            cur_header_index = {}
            cur_num_header = 0
            # Xác định vị trí của từng tiêu đề trong dòng tiêu đề
            for header, variants in header_keywords.items():
                for variant in variants:
                    if header in cur_header_index:
                        break
                    # Tạo biểu thức chính quy cho từng biến thể, chú ý thêm \b để chỉ ranh giới từ
                    pattern = re.compile(r'\b' + re.escape(variant) + r'\b', re.IGNORECASE)
                    match = pattern.search(block_text_lower)
                    if match:
                        for text_idx, text in enumerate(block):
                            if(variant in text.lower()):
                                cur_header_index[header] = text_idx
                                cur_num_header += 1
                                break
            
            if cur_num_header >= num_header:
                header_index = cur_header_index
                num_header = cur_num_header
                header_line = idx

            if any(keyword in block_text_lower for keyword in total_payment_keywords) and total_payment_index == -1:
                total_payment_index = idx

        if ngay != "":
            ngay = ngay + " " + gio
        else:
            ngay = gio
        
        type = 1
        line_after_header = header_line + 1
        if(len(data[line_after_header]) == 1):
            type = 2
        
        if type == 1:
            # type1
            for i in range (header_line + 1, len(data)):
                if(len(data[i]) >= num_header):
                    for price_pattern in price_patterns: 
                        if 'gia' in header_index:
                            price_match = price_pattern.search(data[i][header_index['gia']])
                            if price_match:
                                menu_item = {}
                                if 'ghi_chu' in header_index:
                                    menu_item['name'] = data[i][header_index['ghi_chu']]
                                if 'so_luong' in header_index:
                                    menu_item['quantity'] = data[i][header_index['so_luong']]    
                                menu_item['price'] = data[i][header_index['gia']]
                                menu_items.append(menu_item)
                                break
        else:
            for i in range(header_line + 1, len(data)):
                if(len(data[i]) == 1):
                    count = 2
                    menu_item = {}
                    menu_item['name'] = data[i][0]
                    if 'gia' in header_index:
                        menu_item['price'] = data[i+1][len(data[i+1]) - len(data[header_line]) + header_index['gia']]
                    if 'so_luong' in header_index:
                        menu_item['quantity'] = data[i+1][len(data[i+1]) - len(data[header_line]) + header_index['so_luong']]
                    
                    if i+2 != total_payment_index:
                        for price_pattern in price_patterns: 
                            discount_price_match = price_pattern.search(data[i+2][-1])
                            if discount_price_match:
                                menu_item['discount'] = data[i+2][-1]
                                count += 1
                                break
                
                    i += count
                    menu_items.append(menu_item)
                
                else: 
                    break

        if(total_payment_index != -1):
            if(len(data[total_payment_index]) > 1):
                for price_pattern in price_patterns: 
                    total_payment_match = price_pattern.search(data[total_payment_index][-1])
                    if total_payment_match:
                        tong_tien = data[total_payment_index][-1]
            else:
                for price_pattern in price_patterns: 
                    total_payment_match = price_pattern.search(' '.join(data[total_payment_index + 1]))
                    if total_payment_match:
                        tong_tien = ' '.join(data[total_payment_index + 1])
        else:
            for idx, block in enumerate(data):
                if total_payment_index == -1:
                    block_text = ' '.join(block)  # Nối các phần tử trong block
                    block_text_lower = block_text.lower()
                    if "thanh toán" in block_text_lower:
                        for price_pattern in price_patterns: 
                            total_payment_match = price_pattern.search(data[total_payment_index][-1])
                            if total_payment_match:
                                tong_tien = data[total_payment_index][-1]
                                break
                else:
                    break

        return {
            'Tên quán': ten_quan,
            'Địa chỉ': dia_chi,
            'Thời gian': ngay,
            'Sản phẩm': menu_items,
            'Tổng tiền': tong_tien
        }
    except:
        return {
            'error': True
        }


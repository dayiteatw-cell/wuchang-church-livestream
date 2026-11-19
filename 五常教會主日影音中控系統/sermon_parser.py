# -*- coding: utf-8 -*-
"""
五常教會 PPT 講道題目與講員自動擷取模組
從下載的 PPTX 中自動尋找包含「題目：」的投影片，精準解析：
1. 講道題目（如：人生說明書）
2. 講員牧師（如：施貞同牧師）
並自動組合為 YouTube 直播標題格式。
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

def extract_sermon_info(pptx_path, target_date_str=None):
    """
    從 PPTX 簡報自動解析講道題目與講員
    :param pptx_path: PPTX 檔案完整路徑
    :param target_date_str: 日期字串 (例如 '20261025' 或 None 自動從檔名/當前日期推算)
    :return: dict 包含 title, preacher, formatted_title, date_str
    """
    if not os.path.exists(pptx_path):
        return None

    # 解析日期 (月/日)
    month_day = ""
    if not target_date_str:
        # 從檔名抓取 (例如 20261025.pptx)
        match = re.search(r'(\d{4})(\d{2})(\d{2})', os.path.basename(pptx_path))
        if match:
            month_day = f"{int(match.group(2))}/{int(match.group(3))}"
    else:
        match = re.search(r'(\d{4})?(\d{2})(\d{2})', target_date_str)
        if match:
            month_day = f"{int(match.group(2))}/{int(match.group(3))}"

    if not month_day:
        now = datetime.now()
        month_day = f"{now.month}/{now.day}"

    ns = {
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
    }

    try:
        with zipfile.ZipFile(pptx_path, 'r') as z:
            slide_files = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
            slide_files.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))

            for sf in slide_files:
                xml_data = z.read(sf)
                root = ET.fromstring(xml_data)

                shapes = root.findall('.//p:sp', ns)
                texts = []
                has_topic = False

                for sp in shapes:
                    paras = sp.findall('.//a:p', ns)
                    for p in paras:
                        txt = ''.join([t.text for t in p.findall('.//a:t', ns) if t.text]).strip()
                        if txt:
                            texts.append(txt)
                            if '題目' in txt:
                                has_topic = True

                if has_topic:
                    sermon_title = ''
                    preacher = ''

                    for t in texts:
                        if '題目' in t:
                            continue
                        elif any(k in t for k in ['牧師', '傳道', '長老', '長']):
                            preacher = t
                        else:
                            if not sermon_title:
                                sermon_title = t

                    # 格式化直播標題
                    # 樣式：10/25「人生說明書」施貞同牧師
                    formatted_title = f"{month_day}「{sermon_title}」{preacher}".strip()

                    return {
                        "sermon_title": sermon_title,
                        "preacher": preacher,
                        "month_day": month_day,
                        "youtube_title": formatted_title,
                        "slide_file": sf
                    }
    except Exception as e:
        print(f"解析 PPT 發生錯誤: {e}")
        return None

    return None

if __name__ == "__main__":
    test_path = r"C:\Users\admin\Downloads\20261025.pptx"
    info = extract_sermon_info(test_path)
    if info:
        print("=== 成功擷取主日資訊 ===")
        print(f"講道題目: {info['sermon_title']}")
        print(f"講員牧師: {info['preacher']}")
        print(f"YouTube 直播標題: {info['youtube_title']}")
    else:
        print("未能擷取到資訊。")

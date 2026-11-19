# -*- coding: utf-8 -*-
"""
五常教會 Gmail 主日附件下載模組
自動登入 dayitea.tw@gmail.com (wang) 的「寄件備份」中搜尋主日信件，
支援：
1. 一鍵自動抓取最新主日信件附件（免打日期，全自動判斷最新主日）
2. 指定主日日期（YYYYMMDD）精準下載
下載內容：config.txt, *大綱.docx, *.pptx 至指定資料夾。
"""

import os
import re
import email
from email.header import decode_header
import imaplib
from datetime import datetime, timedelta

def get_recent_sunday():
    """
    智慧計算最適週日日期（格式：YYYYMMDD）
    週日當天：傳回當天
    週一至週三：傳回剛過的這個週日（例如 10/25）
    週四至週六：傳回即將到來的週日（為下週備便）
    """
    today = datetime.now()
    weekday = today.weekday()  # 週一為 0, 週日為 6
    if weekday == 6:
        # 今天就是週日
        target = today
    elif weekday in (0, 1, 2):
        # 週一至週三，預設為剛剛過去的主日
        target = today - timedelta(days=weekday + 1)
    else:
        # 週四至週六，預設為即將到來的主日
        days_ahead = 6 - weekday
        target = today + timedelta(days=days_ahead)
    return target.strftime("%Y%m%d")

def decode_mime_words(raw_text):
    if not raw_text:
        return ""
    decoded = decode_header(raw_text)
    parts = []
    for frag, charset in decoded:
        if isinstance(frag, bytes):
            try:
                parts.append(frag.decode(charset or "utf-8", errors="replace"))
            except Exception:
                parts.append(frag.decode("big5", errors="replace"))
        else:
            parts.append(str(frag))
    return "".join(parts)

DEFAULT_DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

def download_sunday_files(user="dayitea.tw@gmail.com", pwd="tgpl fwhq rbty hpho", target_date=None, save_dir=None, log_callback=print):
    """
    從寄件備份下載主日附件
    :param target_date: 若為 None 或 'LATEST'，自動抓取最新一封主日信件；否則搜尋特定日期 (如 20261025)
    :return: (bool 成功與否, list 下載檔案路徑, str 實際下載的主日日期)
    """
    if save_dir is None:
        save_dir = DEFAULT_DOWNLOAD_DIR
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)

    log_callback(f"連線 Gmail 寄件備份中 (帳號: wang / dayitea.tw@gmail.com)...")

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(user, pwd)

        # 優先定位寄件備份資料夾
        sent_folder = None
        status, folders = mail.list()
        if status == "OK":
            for f in folders:
                f_str = f.decode('utf-8', errors='ignore')
                if r'\Sent' in f_str:
                    parts = f_str.split(' "/" ')
                    if len(parts) == 2:
                        sent_folder = parts[1].strip()
                        break

        if not sent_folder:
            sent_folder = '"[Gmail]/&W8RO9lCZTv0-"'

        res, _ = mail.select(sent_folder)
        if res != "OK":
            for trial in ['"[Gmail]/&W8RO9lCZTv0-"', '"[Gmail]/Sent Mail"', '"[Gmail]/寄件備份"', 'Sent', 'INBOX']:
                res, _ = mail.select(trial)
                if res == "OK":
                    sent_folder = trial
                    break

        target_msg_id = None
        actual_date_str = target_date

        if not target_date or target_date.upper() == 'LATEST':
            # 自動搜尋「最新一封主日信件」
            log_callback("正在寄件備份中檢索 wang 寄出的最新主日信件...")
            status, messages = mail.search(None, 'ALL')
            if status != "OK" or not messages[0]:
                log_callback("[錯誤] 寄件備份中無任何信件！")
                mail.logout()
                return False, [], ""

            mail_ids = messages[0].split()
            # 由新往舊反向搜尋，尋找主旨含有 8 碼日期 (YYYYMMDD) 的信件
            for mid in reversed(mail_ids):
                _, d = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (SUBJECT DATE)])')
                hdr_msg = email.message_from_bytes(d[0][1])
                subj = decode_mime_words(hdr_msg.get('Subject', ''))
                m = re.search(r'(\d{8})', subj)
                if m:
                    target_msg_id = mid
                    actual_date_str = m.group(1)
                    log_callback(f"鎖定最新主日郵件 -> 主旨: [{subj}] (主日日期: {actual_date_str})")
                    break

            if not target_msg_id:
                # 若主旨沒寫日期，取最後一封有附件的信件
                target_msg_id = mail_ids[-1]
                actual_date_str = datetime.now().strftime("%Y%m%d")
                log_callback(f"取最新一封寄件備份 (ID: {target_msg_id.decode()})...")
        else:
            # 依使用者指定的日期搜尋 (例如 20261025)
            log_callback(f"搜尋主旨包含特定日期「{target_date}」的郵件...")
            status, messages = mail.search(None, f'(SUBJECT "{target_date}")')
            if status == "OK" and messages[0]:
                target_msg_id = messages[0].split()[-1]
                actual_date_str = target_date
            else:
                log_callback(f"[提示] 未找到主旨包含 {target_date} 的信件！")
                mail.logout()
                return False, [], target_date

        # 抓取該郵件完整內容與附件
        res, msg_data = mail.fetch(target_msg_id, "(RFC822)")
        if res != "OK":
            log_callback("[錯誤] 讀取信件資料失敗！")
            mail.logout()
            return False, [], actual_date_str

        msg = email.message_from_bytes(msg_data[0][1])
        subject = decode_mime_words(msg.get("Subject", ""))
        log_callback(f"開始解析並下載附件 (信件主旨: {subject})...")

        downloaded_files = []
        for part in msg.walk():
            if part.get_content_maintype() == "multipart" or part.get("Content-Disposition") is None:
                continue

            raw_fn = part.get_filename()
            if raw_fn:
                filename = decode_mime_words(raw_fn)
                filepath = os.path.join(save_dir, filename)

                try:
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    log_callback(f"  [下載成功] -> {filename}")
                    downloaded_files.append(filepath)
                except PermissionError:
                    log_callback(f"  [檔案使用中] -> {filename} 正被 PowerPoint 開啟中，保留現有檔案！")
                    downloaded_files.append(filepath)
                except Exception as fe:
                    log_callback(f"  [檔案寫入錯誤] -> {filename}: {fe}")

        mail.logout()
        log_callback(f"[完成] 全部下載完成！共儲存 {len(downloaded_files)} 個主日檔案至 {save_dir}。")
        return True, downloaded_files, actual_date_str

    except Exception as e:
        log_callback(f"[錯誤] 下載失敗: {e}")
        return False, [], (target_date or "")

if __name__ == "__main__":
    ok, files, d_str = download_sunday_files(target_date=None)
    print("Result:", ok, files, d_str)

# -*- coding: utf-8 -*-
import os
import email
from email.header import decode_header
import imaplib
import sys

GMAIL_USER = "dayitea.tw@gmail.com"
GMAIL_PWD = "tgpl fwhq rbty hpho"
SAVE_DIR = r"C:\Users\admin\Downloads"

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

def main():
    print(f"正在連線至 {GMAIL_USER} ...")
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PWD)
        print("Gmail 登入成功！")

        # 列出所有資料夾以供偵測
        status, folders = mail.list()
        sent_folder = None
        for f in folders:
            f_str = f.decode('utf-8', errors='ignore')
            if r'\Sent' in f_str:
                # 取得資料夾名稱
                # 格式通常為 (\HasNoChildren \Sent) "/" "[Gmail]/Sent Mail"
                parts = f_str.split(' "/" ')
                if len(parts) == 2:
                    sent_folder = parts[1].strip()
                    break

        if not sent_folder:
            sent_folder = '"[Gmail]/Sent Mail"'

        print(f"進入寄件備份資料夾: {sent_folder}")
        res, data = mail.select(sent_folder)
        if res != "OK":
            # 備援嘗試常見名稱
            for trial in ['"[Gmail]/寄件備份"', '"[Gmail]/Sent Mail"', 'Sent', 'INBOX']:
                res, data = mail.select(trial)
                if res == "OK":
                    sent_folder = trial
                    print(f"切換至可用資料夾: {sent_folder}")
                    break

        print("正在搜尋包含 20261025 的信件...")
        status, messages = mail.search(None, '(SUBJECT "20261025")')
        
        if status != "OK" or not messages[0]:
            print("以 SUBJECT 20261025 未找到，嘗試列出最新 5 封寄件信件...")
            status, all_msg = mail.search(None, 'ALL')
            if status == "OK" and all_msg[0]:
                ids = all_msg[0].split()
                latest_ids = ids[-5:]
                for mid in latest_ids:
                    _, mdata = mail.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (SUBJECT DATE TO)])")
                    hdr = mdata[0][1].decode('utf-8', errors='replace')
                    print(f"ID {mid.decode()}: {hdr.strip()}")
            mail.logout()
            return

        mail_ids = messages[0].split()
        print(f"找到 {len(mail_ids)} 封符合信件！處理最後一封最新信件...")
        target_id = mail_ids[-1]

        res, msg_data = mail.fetch(target_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject = decode_mime_words(msg.get("Subject", ""))
        print(f"信件主旨: {subject}")
        print(f"收件者: {decode_mime_words(msg.get('To', ''))}")

        downloaded = []
        for part in msg.walk():
            if part.get_content_maintype() == "multipart" or part.get("Content-Disposition") is None:
                continue

            raw_fn = part.get_filename()
            if raw_fn:
                filename = decode_mime_words(raw_fn)
                filepath = os.path.join(SAVE_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                print(f"  [下載成功] -> {filepath}")
                downloaded.append(filename)

        print(f"\n全部下載完成！共儲存 {len(downloaded)} 個檔案至 {SAVE_DIR}。")
        mail.logout()

    except Exception as e:
        print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()

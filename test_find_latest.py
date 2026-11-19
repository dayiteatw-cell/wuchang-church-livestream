# -*- coding: utf-8 -*-
import imaplib
import email
from email.header import decode_header
import re

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

mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
mail.login('dayitea.tw@gmail.com', 'tgpl fwhq rbty hpho')
mail.select('"[Gmail]/&W8RO9lCZTv0-"')
_, messages = mail.search(None, 'ALL')
ids = messages[0].split()

found_id = None
found_date = None

for mid in reversed(ids):
    _, d = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (SUBJECT DATE)])')
    msg = email.message_from_bytes(d[0][1])
    subj = decode_mime_words(msg.get('Subject', ''))
    m = re.search(r'(\d{8})', subj)
    if m:
        found_id = mid
        found_date = m.group(1)
        print(f"Found latest Sunday email: ID={mid.decode()}, Subject={subj}, Date={found_date}")
        break

mail.logout()

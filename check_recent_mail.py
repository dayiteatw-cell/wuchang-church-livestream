# -*- coding: utf-8 -*-
import imaplib
import email
from email.header import decode_header

def decode_mime(s):
    if not s: return ""
    decoded = decode_header(s)
    parts = []
    for f, c in decoded:
        if isinstance(f, bytes):
            parts.append(f.decode(c or 'utf-8', errors='replace'))
        else:
            parts.append(str(f))
    return "".join(parts)

mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
mail.login('dayitea.tw@gmail.com', 'tgpl fwhq rbty hpho')

for folder in ['"[Gmail]/&W8RO9lCZTv0-"', 'INBOX']:
    typ, _ = mail.select(folder)
    if typ != 'OK':
        print(f"Failed to select {folder}")
        continue
    _, messages = mail.search(None, 'ALL')
    ids = messages[0].split()
    print(f"=== Folder: {folder} (Total: {len(ids)}) ===")
    for mid in ids[-5:]:
        _, d = mail.fetch(mid, '(BODY.PEEK[HEADER.FIELDS (SUBJECT DATE FROM TO)])')
        msg = email.message_from_bytes(d[0][1])
        subj = decode_mime(msg.get('Subject'))
        print(f"  ID {mid.decode()}: Date={msg.get('Date')} | Subject={subj} | To={decode_mime(msg.get('To'))}")

mail.logout()

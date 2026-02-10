import imaplib
import email
from email.header import decode_header
import json

def list_inbox_unread(email_user, app_password):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, app_password)
        mail.select("inbox")
        
        # Search for ALL unread in inbox
        status, messages = mail.search(None, 'UNSEEN')
        if status != 'OK':
            return "Failed to search inbox"
            
        mail_ids = messages[0].split()
        count = len(mail_ids)
        
        samples = []
        # Get up to 20 samples to see what's left
        for i in mail_ids[:20]:
            res, msg_data = mail.fetch(i, "(BODY[HEADER.FIELDS (SUBJECT FROM)])")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg.get("Subject", "No Subject"))[0][0]
                    if isinstance(subject, bytes): subject = subject.decode(errors="replace")
                    sender = decode_header(msg.get("From", "No Sender"))[0][0]
                    if isinstance(sender, bytes): sender = sender.decode(errors="replace")
                    samples.append({"subject": subject, "from": sender})
        
        mail.logout()
        return {"total_unread_in_inbox": count, "samples": samples}
    except Exception as e:
        return f"Error: {str(e)}"

config = {"email": "lvchenkai0812@gmail.com", "app_password": "suyt jxsp xanh fllc"}
print(json.dumps(list_inbox_unread(config["email"], config["app_password"]), ensure_ascii=False, indent=2))

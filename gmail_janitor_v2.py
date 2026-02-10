import imaplib
import email
from email.header import decode_header
import json

def process_inbox(email_user, app_password):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, app_password)
        mail.select("inbox")
        
        status, messages = mail.search(None, 'UNSEEN')
        if status != 'OK':
            return "Failed to search inbox"
            
        mail_ids = messages[0].split()
        if not mail_ids:
            return {"archived": [], "trashed": [], "manual_review": []}
            
        report = {"archived": [], "trashed": [], "manual_review": []}
        
        auto_archive_keywords = ["linkedin", "coursera", "newsletter", "update", "digest", "notification", "weekly", "daily", "alert", "monitoring", "subscription", "promotion"]
        auto_trash_keywords = ["unsubscribe", "ad ", "offer", "discount", "sale", "shopping", "marketing", "advertisement"]
        value_keywords = ["receipt", "invoice", "payment", "bank", "statement", "important", "security", "action required", "urgent", "password", "login", "verification", "2fa"]

        # Limit to 50 messages to avoid timeout
        for i in mail_ids[:50]:
            res, msg_data = mail.fetch(i, "(BODY[HEADER.FIELDS (SUBJECT FROM)])")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg.get("Subject", ""))[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="replace")
                    
                    sender, encoding = decode_header(msg.get("From", ""))[0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding if encoding else "utf-8", errors="replace")
                    
                    text_to_check = (str(subject) + " " + str(sender)).lower()
                    
                    action = "review"
                    if any(val in text_to_check for val in value_keywords):
                        action = "review"
                    elif any(trash in text_to_check for trash in auto_trash_keywords):
                        action = "trash"
                    elif any(arch in text_to_check for arch in auto_archive_keywords):
                        action = "archive"
                    
                    if action == "archive":
                        mail.store(i, '+FLAGS', '\\Seen')
                        mail.store(i, '+FLAGS', '\\Deleted')
                        report["archived"].append(f"{subject} (from {sender})")
                    elif action == "trash":
                        mail.store(i, '+FLAGS', '\\Deleted')
                        report["trashed"].append(f"{subject} (from {sender})")
                    else:
                        report["manual_review"].append({"subject": subject, "from": sender})
        
        mail.expunge()
        mail.logout()
        return report
    except Exception as e:
        return f"Error: {str(e)}"

config = {"email": "lvchenkai0812@gmail.com", "app_password": "suyt jxsp xanh fllc"}
result = process_inbox(config["email"], config["app_password"])
print(json.dumps(result, ensure_ascii=False, indent=2))

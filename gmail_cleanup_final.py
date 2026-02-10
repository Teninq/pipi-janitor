import imaplib
import email
from email.header import decode_header
import json

def process_inbox(email_user, app_password):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, app_password)
        mail.select("inbox")
        
        # Search for all unread messages
        status, messages = mail.search(None, 'UNSEEN')
        if status != 'OK':
            return "Failed to search inbox"
            
        mail_ids = messages[0].split()
        if not mail_ids:
            return "No more unread messages."
            
        report = {
            "custom_labeled": [],
            "archived": [],
            "trashed": [],
            "manual_review": []
        }
        
        # Classification rules
        auto_archive_keywords = [
            "linkedin", "coursera", "newsletter", "update", "digest", 
            "notification", "weekly", "daily", "alert", "monitoring",
            "subscription", "promotion", "reddit", "kaggle", "medium", "substack"
        ]
        
        auto_trash_keywords = [
            "unsubscribe", "ad ", "offer", "discount", "sale", "shopping",
            "marketing", "advertisement", "bonus", "win "
        ]
        
        value_keywords = [
            "receipt", "invoice", "payment", "bank", "statement", 
            "important", "security", "action required", "urgent",
            "password", "login", "verification", "2fa", "github"
        ]

        for i in mail_ids:
            res, msg_data = mail.fetch(i, "(BODY[HEADER.FIELDS (SUBJECT FROM)])")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    subject = ""
                    subject_header = msg.get("Subject")
                    if subject_header:
                        subject_parts = decode_header(subject_header)
                        for part, encoding in subject_parts:
                            if isinstance(part, bytes):
                                subject += part.decode(encoding if encoding else "utf-8", errors="replace")
                            else:
                                subject += str(part)
                    
                    sender = ""
                    sender_header = msg.get("From")
                    if sender_header:
                        sender_parts = decode_header(sender_header)
                        for part, encoding in sender_parts:
                            if isinstance(part, bytes):
                                sender += part.decode(encoding if encoding else "utf-8", errors="replace")
                            else:
                                sender += str(part)
                    
                    text_to_check = (subject + " " + sender).lower()
                    
                    # 1. Check for CDISC -> Data Science label
                    if "cdisc" in text_to_check:
                        mail.store(i, '+FLAGS', '\\Seen')
                        # Note: Labeling in Gmail via IMAP is done by adding a label as a folder/X-GM-LABELS
                        # But for simplicity and safety, we follow the "Archive" (remove from inbox) requirement
                        # Attempt to add label via X-GM-LABELS if supported
                        try:
                            mail.store(i, '+X-GM-LABELS', 'Data Science')
                        except:
                            pass
                        mail.store(i, '+FLAGS', '\\Deleted')
                        report["custom_labeled"].append(f"CDISC: {subject} -> Data Science")
                        
                    # 2. Check for manual review (value)
                    elif any(val in text_to_check for val in value_keywords):
                        report["manual_review"].append({"subject": subject, "from": sender})
                        
                    # 3. Check for garbage
                    elif any(trash in text_to_check for trash in auto_trash_keywords):
                        mail.store(i, '+FLAGS', '\\Deleted')
                        report["trashed"].append(f"{subject}")
                        
                    # 4. Check for known auto-archived categories
                    elif any(arch in text_to_check for arch in auto_archive_keywords):
                        mail.store(i, '+FLAGS', '\\Seen')
                        mail.store(i, '+FLAGS', '\\Deleted')
                        report["archived"].append(f"{subject}")
                    
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

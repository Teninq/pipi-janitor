import imaplib
import email
from email.header import decode_header
import json

def get_gmail_messages(email_user, app_password, search_query):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_user, app_password)
        mail.select("inbox")
        
        status, messages = mail.search(None, search_query)
        if status != 'OK':
            return []
            
        mail_ids = messages[0].split()
        results = []
        
        # Get last 10 messages for each category to keep it concise
        for i in mail_ids[-10:]:
            res, msg_data = mail.fetch(i, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    # Extract body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    results.append({"subject": subject, "body": body[:500]}) # Truncate body
        
        mail.logout()
        return results
    except Exception as e:
        return str(e)

config = [
    {"email": "lvchenkai0812@gmail.com", "app_password": "suyt jxsp xanh fllc"}
]

linkedin_mails = get_gmail_messages(config[0]["email"], config[0]["app_password"], '(UNSEEN FROM "LinkedIn")')
coursera_mails = get_gmail_messages(config[0]["email"], config[0]["app_password"], '(UNSEEN FROM "Coursera")')

print(json.dumps({"linkedin": linkedin_mails, "coursera": coursera_mails}, ensure_ascii=False))

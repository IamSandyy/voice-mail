import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import decode_header
from CONSTANTS import EMAIL_ID, PASSWORD
from voice_utils import SpeakText,speech_to_text

def sendMail(to, subject, body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ID, PASSWORD)
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ID
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server.sendmail(EMAIL_ID, to, msg.as_string())
        server.quit()
        SpeakText("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
        SpeakText("Failed to send email.")

def composeMail():
    SpeakText("Please say the recipient's email address.")
    to = speech_to_text()
    
    if to:
        to = to.lower().replace(" at ", "@").replace(" dot ", ".").replace(" ", "")
        SpeakText(f"Using email: {to}")
        
        SpeakText("Please say the subject.")
        subject = speech_to_text()
        SpeakText("Please say the body of the email.")
        body = speech_to_text()
        
        try:
            sendMail(to, subject, body)
            return True  # Email sent successfully
        except Exception as e:
            print(f"Error sending email: {e}")
            return False  # Email sending failed
    return False  # Invalid email input

def getMailBoxStatus():
    try:
        with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
            mail.login(EMAIL_ID, PASSWORD)
            status, response = mail.select("inbox")
            mailbox_status = f"You have {response[0].decode()} messages in your inbox."
            SpeakText(mailbox_status)
            return mailbox_status
    except Exception as e:
        print(f"Error fetching mailbox status: {e}")
        SpeakText("Could not retrieve mailbox status.")
        return "Mailbox status could not be retrieved."

def getLatestMails():
    try:
        with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
            mail.login(EMAIL_ID, PASSWORD)
            mail.select("inbox")
            status, messages = mail.search(None, 'ALL')
            messages = messages[0].split()[-3:]  # Get the last 3 messages
            latest_emails = []
            for num in messages:
                status, msg_data = mail.fetch(num, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        from_ = msg.get("From")
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        latest_emails.append({
                            "from": from_,
                            "subject": subject
                        })
            return latest_emails
    except Exception as e:
        print(f"Error retrieving emails: {e}")
        SpeakText("Could not retrieve emails.")
        return None
    
def findMail(search_query):
    try:
        with imaplib.IMAP4_SSL("imap.gmail.com") as mail:
            mail.login(EMAIL_ID, PASSWORD)
            mail.select("inbox")

            # Search emails by subject or sender
            search_criteria = f'(OR SUBJECT "{search_query}" FROM "{search_query}")'
            status, messages = mail.search(None, search_criteria)

            if status == "OK":
                messages = messages[0].split()
                if not messages:
                    SpeakText("No emails found with the given search query.")
                    return None

                # Fetch the first found email (you can modify to fetch more)
                latest_emails = []
                for num in messages[:3]:  # Limit to the first 3 results
                    status, msg_data = mail.fetch(num, "(RFC822)")
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            from_ = msg.get("From")
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else "utf-8")
                            latest_emails.append({
                                "from": from_,
                                "subject": subject
                            })
                return latest_emails
            else:
                SpeakText("Error searching for emails.")
                return None
    except Exception as e:
        print(f"Error finding emails: {e}")
        SpeakText("Could not retrieve emails.")
        return None

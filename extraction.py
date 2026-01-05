import os
import imaplib
import email
import asyncio
import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr
import concurrent.futures
from dotenv import load_dotenv

load_dotenv()

class EmailFetcher:
    def __init__(self, host, user, password, smtp_server):
        self.host = os.getenv("IMAP_HOST")
        self.user = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = os.getenv("SMTP_SERVER")

        # Debug prints
        # print(f"IMAP_HOST: {self.host}")
        # print(f"EMAIL_USER: {self.user}")
        # print(f"EMAIL_PASSWORD: {'*' * len(self.password) if self.password else 'None'}")
        # print(f"SMTP_SERVER: {self.smtp_server}")

        with open('whitelist.yaml','r') as file:
            data = yaml.safe_load(file)
            self.whitelist = set(data.get('whitelist', []))

    def login(self):
        print(f"Connecting to {self.host}...")
        mail = imaplib.IMAP4_SSL(self.host, timeout=30)
        print("Connected! Logging in...")
        mail.login(self.user, self.password)
        print("Login successful! Selecting inbox...")
        mail.select("inbox")
        print("Inbox selected!")
        return mail
    
    async def fetch_new_emails(self):
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            new_emails = await loop.run_in_executor(pool, self._fetch_new_emails_sync)
        return new_emails
    
    def _fetch_new_emails_sync(self):
        mail = self.login()
        print("Searching for unread emails...")
        response, email_ids_bytes = mail.uid('search', None, 'UNSEEN')
        print(f"Search complete! Response: {response}")
        if response != 'OK':
            print("Failed to retrieve emails.")
            return []
        
        email_ids = email_ids_bytes[0].decode('utf-8').split()
        print(f"Found {len(email_ids)} unread email(s)")

        if len(email_ids) == 0:
            print("No new emails found.")
            return []
        
        new_emails = []
        for e_id in email_ids:
            response, msg_data = mail.uid('fetch', e_id, '(BODY[])')
            if response != 'OK':
                print(f"Failed to fetch email with ID {e_id}.")
                continue
            
            email_msg = email.message_from_bytes(msg_data[0][1])
            sender_name, sender_addr = parseaddr(email_msg['From'])

            new_emails.append((email_msg, sender_name, sender_addr))
            mail.uid('store', e_id, '+FLAGS', '(\\Seen)')

        mail.logout()
        return new_emails
    
    def send_email(self, recipient, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(self.smtp_server, 587) as server:
            server.starttls()
            server.login(self.user, self.password)
            text = msg.as_string()
            server.sendmail(self.user, recipient, text)
            server.quit()
            
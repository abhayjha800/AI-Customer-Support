from extraction import EmailFetcher
from support import AICustomerSupport
import asyncio
from dotenv import load_dotenv


async def fetch_and_process_emails(fetcher, ai_support):
    while True:
        print("Checking for new emails...")
        new_emails = await fetcher.fetch_new_emails()
        for email_message, sender_name, sender_addr in new_emails:
            if sender_addr not in fetcher.whitelist:
                print(f"Sender {sender_addr} not in whitelist. Skipping email.")
                continue

            print(f"Processing email from {sender_addr}...")
            extracted, reply_content = await ai_support.process_email(email_message)
            print(f"Reply to {sender_addr}:\n{reply_content}\n")

            subject = "AI customer service reply"
            fetcher.send_email(sender_addr, subject, reply_content)

        await asyncio.sleep(10)  # Check for new emails every 60 seconds


async def main():
    load_dotenv()

    fetcher = EmailFetcher(
        host=None,
        user=None,
        password=None,
        smtp_server=None
    )
    ai_support = AICustomerSupport()

    await fetch_and_process_emails(fetcher, ai_support)

if __name__ == "__main__":
    asyncio.run(main())
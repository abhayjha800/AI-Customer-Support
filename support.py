from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()



class EmailProperties(BaseModel):
    category: Literal[
        "complaint",
        "refund_request",
        "product_feedback",
        "customer_service_inquiry",
        "others",
    ] = Field(description="Category of the email")

    mentioned_products: str = Field(description="Products mentioned in the email")

    issue_description: str = Field(description="Description of the issue raised in the email")

    name: str = Field(description="Name of the customer who wrote the email")


class AICustomerSupport:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

        # LLM that RETURNS structured output
        self.extractor = self.llm.with_structured_output(EmailProperties)

        self.reply_prompt = ChatPromptTemplate.from_template(
            """
            You are an AI Customer Support agent.

            Address the user by name: {name}.
            If no name is provided, say "Dear customer".

            Category: {category}
            Product mentioned: {mentioned_products}
            Issue: {issue_description}

            Write a friendly and helpful reply.
            Include:
            - Understanding of the issue
            - A proposed solution
            - A polite sign-off

            Sign the email as "John Doe".
            """
        )

        self.reply_chain = self.reply_prompt | self.llm

    def get_email_content(self, email_message):
        """Extract text content from email message"""
        if email_message.is_multipart():
            # For multipart emails, iterate through parts
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    try:
                        return part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        return part.get_payload()
        else:
            # For simple emails, get payload directly
            try:
                payload = email_message.get_payload(decode=True)
                if isinstance(payload, bytes):
                    return payload.decode('utf-8', errors='ignore')
                return payload
            except:
                return email_message.get_payload()
        
        # Fallback if no text/plain found
        return "No readable content found in email"
        
        
    async def process_email(self, email_message):
        email_content = self.get_email_content(email_message)

        # Structured extraction
        extracted: EmailProperties = await self.extractor.ainvoke(email_content)

        # Generate reply
        reply = await self.reply_chain.ainvoke(extracted.model_dump())

        return extracted, reply.content

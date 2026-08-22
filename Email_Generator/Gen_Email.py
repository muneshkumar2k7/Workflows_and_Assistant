from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel , Field , EmailStr
from typing import Literal , Annotated

load_dotenv()


llms = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

prompt = ChatPromptTemplate.from_template(
    """
You are an expert professional email writer.

Your task is to write a clear, polished, and natural email using ONLY
the information provided below.

IMPORTANT RULES:
1. Do not invent facts, names, dates, promises, achievements, or details.
2. Do not add information that is not provided by the user.
3. Keep the meaning and purpose of the user's information unchanged.
4. Correct grammar, spelling, punctuation, and awkward phrasing.
5. Make the email sound natural, professional, and respectful.
6. Follow the requested tone exactly.
7. Follow the requested length.
8. Organize the email logically with appropriate paragraphs.
9. Include an appropriate greeting and closing.
10. Do not explain what you changed.
11. Return ONLY the final email.

EMAIL INFORMATION:

Recipient: {Recipient}
Topic: {topic}
Purpose: {purpose}
Details: {details}
Tone: {tone}
Length: {length}

Write the final email now.
"""
)

class Email(BaseModel):
    topic : Annotated[str , Field(description= "Enter the topic only not anything else" , examples=["Exercise"])]
    Recipient : EmailStr
    tone: Annotated[
    Literal["Casual", "Professional", "Friendly"],
    Field(description="Choose the email tone")
    ]
    
    length : Annotated[ 
    Literal["short", "medium","long"],
    Field(description= "choose the email tone")]
    details : Annotated [ str , Field(description= "detail of the email ")]
    purpose : Annotated[ str , Field(description= "subject of the email or purpose")]
    









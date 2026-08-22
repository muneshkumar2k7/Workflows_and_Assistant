from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel , Field
from typing import Literal 

load_dotenv()


llms = ChatGoogleGenerativeAI(
    model = "Gemini Flash 2.5"
)

class ActionItem(BaseModel):
    Task: str
    owner : str
    Deadline : str  


class MeetingSummary(BaseModel):
    summary : str
    decision : list[str]
    items : list[ActionItem]


prompt = ChatPromptTemplate.from_template(
    """
You are Meeting Notes Summarizer:

Notes : {Notes}

Tasks need to do:
Summary 
decisions
action items (Task ,Person , Deadlines)

"""
)

structured_llms=llms.with_structured_output(MeetingSummary)
chain = prompt | structured_llms

while True:
    query = input("Enter the Notes (q to quit): ")

    if query.lower() == "q":
        break

    ans = chain.invoke({
        "Notes": query
    })

    print(ans.model_dump())


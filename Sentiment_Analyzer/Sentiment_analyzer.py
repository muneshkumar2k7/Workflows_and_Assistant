from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel , Field
from typing import Literal , Optional



load_dotenv()


llms = ChatGoogleGenerativeAI(
     model="gemini-2.5-flash"
)


prompt = ChatPromptTemplate.from_template(
    """
 You are Sentiment Analyzer:
 Analyze the Sentiment of the given Text :
 Text :{text}
"""
)

class Sentiment(BaseModel): 
     Sentiments : Literal["Positive","Negative","Neutral"]


structured_llms = llms.with_structured_output(Sentiment)

chain = prompt | structured_llms

while True:
    query = input("Enter the text (q to quit): ")

    if query.lower() == "q":
        break

    ans = chain.invoke({"text": query})

    print(ans.model_dump())
     
     







    
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
    You are JSON OUTPUT GENERATOR:
    Convert Given text in Json Format:

    Text : {text}
"""
)

class JsonSchema(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0, lt=100)
    city:  Optional[str] = None
    skill:  Optional[str] = None



structuredllms =llms.with_structured_output(JsonSchema)


while True:
    input_text = input("Enter the text")

    if input_text.lower() == "q":
          break

    
    query = prompt.invoke({"text": input_text})
    ans=structuredllms.invoke(query)
    print(ans.model_dump())
    
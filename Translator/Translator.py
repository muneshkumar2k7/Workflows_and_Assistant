from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel , Field
from typing import Literal 

load_dotenv()

class Language_schema(BaseModel):
    language  :  Literal[
    "English",
    "Urdu",
    "Hindi",
    "Arabic",
    "Spanish",
    "French",
    "German",
    "Chinese",
    "Japanese",
    "Korean"
]

llms = ChatGoogleGenerativeAI(
    model = "Gemini Flash 2.5"
)


prompt = ChatPromptTemplate.from_template(
    """
   You are language Translator:

   Translate the given text into the mentioned language:

   Text : {text}
   Language : {language}

"""
) 


while True:
     input_text = input("Enter the Text (Enter q to quit)")
     input_language = input("Enter the language")

     if input_text.lower() == "q":
          break

     lang = Language_schema(
          language_list= input_language
     )
     query = prompt.invoke({"text": input_text , "Language":lang.language})
     response =llms.invoke(query)
     print(response.content)
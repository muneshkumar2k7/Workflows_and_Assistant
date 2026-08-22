from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel , Field
from typing import Annotated , Literal
load_dotenv()


llms = ChatGoogleGenerativeAI(
      model = "Gemini Flash 2.5"
) 


class Title(BaseModel):
    Topic : str  
    Audience : Literal["Beginner" , "Proffessional", "Researcher"]
    Tone : Literal["Friendly", "Proffessional"]
    Number_of_titles:  Annotated[int, Field(gt = 0 , lt =10)]
    


class Gen_title_schema(BaseModel):
    Generated_titles : list[str]


class Style_schema(BaseModel):
    Styles: list[str]

class Score_schema(BaseModel):
    Score : list[int]


class Reason_schema(BaseModel):
    Reason : list[str]


class Response_schema(BaseModel):
    Generated_titles : list[str] 
    Reasons : list[str]
    Scores : list[int]
    Styles : list[str]



Gen_title_prompt = ChatPromptTemplate.from_template(
"""
 You are Blog Title Generator
 Generate {Number_of_titles} related to Given Topic  {Topic} 
  Consider  : Audience {Audience} and Tone {Tone}

  please be strict to the above conditions 
"""
)


Gen_style_prompt = ChatPromptTemplate.from_template(
    """
Generate one style for each Title 
these are number of titles {Number_of_titles}
this is the list of titles {Generated_titles}
"""
)


Gen_Score_prompt = ChatPromptTemplate.from_template(
    """
Generate score out of 10 for each Title 
these are number of titles {Number_of_titles}
this is the list of titles {Generated_titles}
"""
)


Gen_Reason_prompt = ChatPromptTemplate.from_template(
    """
Generate one reason for each Title 
these are number of titles {Number_of_titles}
this is the list of titles {Generated_titles}

please consider all above points.
"""
)




while True:
   Topic = input("Enter the topic (q to quit): ")

   if Topic.lower() == "q":
        break
   Aud =  input("Choose the Audience ['Beginner' , 'Proffessional', 'Researcher']")
   Tone =  input("Enter the Tone ['Friendly', 'Proffessional']")
   Number_of_titles =  input("Enter the Number of titles you want")

   user_input = Title(
    Topic=Topic,
    Audience=Aud,
    Tone=Tone,
    Number_of_titles=int(Number_of_titles)
)
   
   title_prompt = Gen_title_prompt.invoke({
       "Topic":user_input.Topic,
       "Audience" : user_input.Audience,
       "Tone": user_input.Tone,
       "Number_of_titles":user_input.Number_of_titles
   })

   Title_llms =llms.with_structured_output(Gen_title_schema)
   Gen_title_response = Title_llms.invoke(title_prompt)

   style_prompt =Gen_style_prompt.invoke({
       "Number_of_titles":Number_of_titles , 
       "Generated_titles" : Gen_title_response.Generated_titles
   })

   Stylellms = llms.with_structured_output(Style_schema)
   Style_response = Stylellms.invoke(style_prompt)


   score_prompt = Gen_Score_prompt.invoke({
       "Number_of_titles":Number_of_titles , 
       "Generated_titles" : Gen_title_response.Generated_titles
   })

   Scorellms = llms.with_structured_output(Score_schema)
   Score_response = Scorellms.invoke(score_prompt)   

   Reason_prompt = Gen_Reason_prompt.invoke({
       "Number_of_titles":Number_of_titles , 
       "Generated_titles" : Gen_title_response.Generated_titles
   })

   Reasonllms = llms.with_structured_output(Reason_schema)
   Reason_response = Reasonllms.invoke(Reason_prompt)  

   Final_Response=Response_schema(
       Generated_titles= Gen_title_response.Generated_titles,
       Reasons = Reason_response.Reason,
       Scores = Score_response.Score ,
       Styles= Style_response.Styles
   )

   print(Final_Response.model_dump())
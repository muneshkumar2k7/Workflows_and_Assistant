from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel , Field
from typing import Literal
load_dotenv()

llms = ChatGoogleGenerativeAI(
    model = "Gemini Flash 2.5"
)

class Resume(BaseModel):
    Bullet : str 
    Job_role : Literal[ "Software Engineer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Data Scientist",
    "Data Analyst"]


prompt = ChatPromptTemplate.from_template(
    """ 
You are a Resume Bullet Improver.

Improve the given resume bullet for the specified job role.

Job Role:
{role}

Resume Bullet:
{bullet}

Rules:
- Preserve the original meaning.
- Make the bullet professional and concise.
- Use strong action verbs.
- Tailor the wording to the job role.
- Do not invent metrics, achievements, technologies, or responsibilities.
"""
)



while True:
    query = input("Enter the Resume to End the conversation type ('q' to quit) ")
    if query.lower() == 'q':
        break

    job = input("Enter the Job role")
    r = Resume(
        Bullet = query,
        Job_role= job
            )
    
    p = prompt.invoke(r.model_dump())

    ans =llms.invoke(p)
    print(ans.content)
    
    
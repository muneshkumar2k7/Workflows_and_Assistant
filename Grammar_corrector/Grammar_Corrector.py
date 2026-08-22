from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel , Field
from typing import Annotated
load_dotenv()

llms = ChatGoogleGenerativeAI(
      model = "Gemini Flash 2.5"
)

class Grammar(BaseModel):
    text : Annotated[str, Field(description = "The grammatically corrected version of the user's text")]
    score : Annotated[int,  Field(
    description="Grammar score from 0 to 10",
    ge=0,
    le=10
) ]
    
    explanation : list[str]
    mistake  : list[str]




class Mistakes_schema(BaseModel):
      string : list[str]


class explanation_schema(BaseModel):
      string : list[str]

class ScoreSchema(BaseModel):
    score: int = Field(
        description="Grammar score from 0 to 10",
        ge=0,
        le=10
    )

mistakes = ChatPromptTemplate.from_template(
    """
    You are Assistant who preform Grammar Correction 
    Your tasks is:
    detect grammatical mistakes {text}  
"""
)


correction = ChatPromptTemplate.from_template(
    """
    You are Assistant who preform Grammar Correction 
    Your tasks is:
    Provide Correction for Given Mistakes : {mistakes} in the text below :
    {text}
     
"""
)



score = ChatPromptTemplate.from_template(
    """
    You are Assistant who preform Grammar Correction 
    Your tasks is:
     Score as Grammar lecturer out of 10 after noticing mistakes {mistakes} and text {text} 
"""
)



corrected = ChatPromptTemplate.from_template(
    """
    You are Assistant who preform Grammar Correction 
    Your tasks is:
     Provided the text after improving grammar mistakes in text {text}

    Strict :  Don't change the context only provided Accurate version of this text. 
"""
)



while True:
    question = input("Enter the text (q to quit): ")

    if question.lower() == "q":
        break

    problem_prompt = mistakes.invoke({
        "text": question
    })

    llms_structured = llms.with_structured_output(Mistakes_schema)
    problem = llms_structured.invoke(problem_prompt)

    explanation_prompt = correction.invoke({
        "text": question,
        "mistakes": problem.string
    })

    llms_structured = llms.with_structured_output(explanation_schema)
    explanation = llms_structured.invoke(explanation_prompt)

    number = score.invoke({
        "text": question,
        "mistakes": problem.string
    })

    score_llm = llms.with_structured_output(ScoreSchema)
    num = score_llm.invoke(number)

    improved_version = corrected.invoke({
        "text": question
    })

    response_text = llms.invoke(improved_version)

    g = Grammar(
        text=response_text,
        score=num.score,
        explanation=explanation.string,
        mistake=problem.string,
    )

    print(g.model_dump())
        
from langchain_core.prompts import Prompt
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.messages import HumanMessage , AIMessage  , ToolMessage
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

ChatGoogleGenerativeAI(
    model = "Gemini-Flash 2.5",
)


class Stack:

  def __init__(self):
     self.arr= []
     self.top = -1

  def push(self, value):
     self.arr.append(value)
     self.top = self.top + 1

  def pop(self):
     if self.top == -1:
        return None

     else :

       value = self.arr[self.top]
       self.top = self.top -1
       return value
     

  def peek(self):

      if self.top == -1:
         return None

      else :
         return self.arr[self.top]




  def is_empty(self):
        return self.top == -1





    


def precedence(operator):

   def precedence(operator):

    if operator == "+" or operator == "-":
        return 1

    elif operator == "*" or operator == "/" or operator == "%":
        return 2

    return 0


def calculate(numbers, operator):

    b = numbers.pop()
    a = numbers.pop()

    op = operator.pop()

    if op == "+":
        result = a + b

    elif op == "-":
        result = a - b

    elif op == "*":
        result = a * b

    elif op == "/":
        result = a / b

    elif op == "%":
        result = a % b

    numbers.push(result)






llms = ChatGoogleGenerativeAI(
    model = "Gemini Flash 2.5"
)




@tool
def calculator(expression: str):
    """Calculate a mathematical expression."""

    numbers = Stack()
    operator = Stack()
    n =""
    i = 0

    while i < len(expression):

        if expression[i].isdigit():
           n += expression[i]

        else:
         if n != "":
          numbers.push(int(n))
          n = ""

         if expression[i] == "(":
           operator.push("(")

         elif expression[i] ==")":
           
               while(
                not operator.is_empty()  and  operator.peek() != "("
                ):
                  calculate(numbers, operator)
                       

               if not operator.is_empty() and operator.peek() == "(":
                   operator.pop()

         else:
              while (
                    not operator.is_empty()
                    and operator.peek() != "("
                     and precedence(operator.peek()) >= precedence(expression[i])
                ):
               calculate(numbers, operator)

              operator.push(expression[i])

    i += 1

    
    if n != "":
        numbers.push(int(n))

    while not operator.is_empty():

        calculate(numbers, operator)

    return numbers.pop()






agent  = create_agent(
    model = llms,
    tools= [calculator],
    system_prompt=  """
    You are a calculator assistant.
    Use the calculator tool whenever mathematical calculation is required.
    Do not calculate the result yourself.
    """
)


while True:
    question = input("Give me the math (q to quit): ")

    if question.lower() == "q":
        break

    agent.invoke({
        "message": [
            HumanMessage(content=question)
        ]
    })
 






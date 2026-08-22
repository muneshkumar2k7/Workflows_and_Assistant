from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llms = ChatGoogleGenerativeAI(
    model = "Gemini Flash 2.5"
)

prompt = ChatPromptTemplate.from_template("""
You are a helpful text summarization assistant.
Summarize the given text accurately.
Do not add information that is not present in the text.

Summarize the given Text: {text}
""")


while True:
    query = input("Give the text to summarize Enter(q to quit the chat)")

    if query.lower() == "q": 
        break

    pr = prompt.invoke({"text":query})

    response = llms.invoke(pr)
    print("\nSummary:")
    print(response.content)


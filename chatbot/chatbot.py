from langgraph.graph import StateGraph ,START , END
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage  
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages


llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
   google_api_key="AIzaSyDlc20LjO0fjtnlS5qBRnaX1WcCz7hayNw"
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]


def Chat(state: ChatState)->ChatState:
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages':[response]}


Graph = StateGraph(ChatState)

Graph.add_node('Chat_node',Chat)
Graph.add_edge(START,'Chat_node')
Graph.add_edge('Chat_node',END)



workflow = Graph.compile()

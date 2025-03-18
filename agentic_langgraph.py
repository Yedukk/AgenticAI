from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages

from IPython.display import Image, display

import os
from langchain_groq import ChatGroq


LANGSMITH_TRACING="true"
LANGSMITH_API_KEYs= os.environ.get("LANGSMITH_API_KEY")
LANGSMITH_PROJECT="TestingLLM"

grok_api_keys = os.environ.get("GROK_API_KEY")
if not grok_api_keys:
    raise ValueError("Missing 'grok_api_key'. Set it in environment variables.")

llm = ChatGroq(api_key=grok_api_keys, model_name="gemma2-9b-it")


class State(TypedDict):
    messages: Annotated[list,add_messages]

def chatbot(state:State):
    return {"messages":llm.invoke(state["messages"])}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot",END)

graph = graph_builder.compile()

# img = Image("/image.jpg")
# with open("output_image.jpg", "wb") as f:
#     f.write(img.data)

while True:
    user_input= input("User: ")
    if user_input.lower() in ["quit","q","e","exit"]:
        print("Good bye..!")
        break
    for event in graph.stream({"messages": ("user", user_input)}):
        print(event.values())
        for value in event.values():
            print(value['messages'])
            print("Assistant: ",value['messages'].content)
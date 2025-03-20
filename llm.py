from langchain_groq import ChatGroq
from config import GROK_API_KEYs

llm = ChatGroq(api_key=GROK_API_KEYs, model_name="gemma2-9b-it")

# def invoke_llm_stream(messages):
#     """General message using LLM"""
#     return llm.stream(messages)

def invoke_llm_stream(messages):
    """General message using LLM"""
    response = []
    for chunk in llm.stream(messages):  # Stream messages
        response.append(chunk)  # Collect them into a list
    return response

def summarize_text(text, query):
    """Summarizes the given text using LLM."""
    summary_prompt = f"Summarize this content:{text} according to user query {query}"
    response = []
    for chunk in llm.stream(summary_prompt):
        response.append(chunk)  # Collect them into a list
    return response

def classify_query(user_input):
    """Classifies the user query as 'chat' or 'web' using LLM."""
    prompt = f"Determine if this query is about general conversation or if it requires vector data.\nQuery: {user_input}\nRespond with 'chat' or 'vector' only."
    response = llm.invoke([{"role": "system", "content": prompt}])
    print("Classifies::",response.content.strip().lower())
    return response.content.strip().lower()
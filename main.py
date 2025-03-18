from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from graph import chat_graph
import asyncio

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.post("/chat")
async def chat_endpoint(user_input: str):
    """Handles chatbot queries with streaming response."""
    state = {"messages": [{"role": "user", "content": user_input}]}

    async def event_stream():
        for event in chat_graph.stream(state):
            for value in event.values():
                for message in value["messages"]:  
                    yield f"{message.content}\n"  # Send each chunk
                    await asyncio.sleep(0.1)  # Prevent buffering

    return StreamingResponse(event_stream(), media_type="text/event-stream")

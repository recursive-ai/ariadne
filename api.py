from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from ariadne import query_ariadne
from db import create_conversation, get_conversation

app = FastAPI()


class ConversationInput(BaseModel):
    conversation_id: int
    user_input: str


@app.post("/create_conversation")
async def create_new_conversation():
    conversation_id = create_conversation()
    return {"conversation_id": conversation_id}


@app.post("/converse")
async def converse(input: ConversationInput):
    try:
        response = query_ariadne(input.conversation_id, input.user_input)
        return {"ariadne": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/conversation/{conversation_id}")
async def get_conversation_history(conversation_id: int):
    try:
        conversation = get_conversation(conversation_id)
        return {"conversation": conversation}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Conversation not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

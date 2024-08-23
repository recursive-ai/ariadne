from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ariadne import query_ariadne

app = FastAPI()

class ConversationInput(BaseModel):
    user_input: str

@app.post("/converse/")
async def converse(input: ConversationInput):
    user_input = input.user_input
    response = query_ariadne(user_input)
    return {"ariadne": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from pydantic import BaseModel


class ChatRequest(BaseModel):
    userId: str
    conversationId: str
    prompt: str


class ChatResponse(BaseModel):
    response: str
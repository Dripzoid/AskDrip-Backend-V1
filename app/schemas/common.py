from pydantic import BaseModel
from typing import Any, Optional


# STANDARD API RESPONSE
class ApiResponse(BaseModel):

    success: bool
    message: str

    route: Optional[str] = None

    response_time: Optional[str] = None

    data: Optional[Any] = None


# COMMON PROMPT REQUEST
class PromptRequest(BaseModel):

    userId: str
    conversationId: str
    prompt: str


# OPTIONAL HEALTH RESPONSE
class HealthResponse(BaseModel):

    status: str
    app_name: str
    version: str
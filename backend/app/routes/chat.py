import logging

from fastapi import APIRouter, HTTPException

from ..models.schemas import ChatRequest, ChatResponse
from ..services import retriever

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    text = req.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="message must not be empty")

    try:
        answer, alternate, qid, aid = retriever.chatbot_response_for_api(text)
    except Exception:
        logger.exception("chatbot_response failed")
        raise HTTPException(status_code=500, detail="Chat inference failed") from None

    return ChatResponse(
        answer=str(answer),
        alternate=alternate,
        qid=int(qid),
        aid=int(aid),
    )

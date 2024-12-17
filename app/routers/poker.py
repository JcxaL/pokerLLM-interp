import json
from fastapi import APIRouter, UploadFile, File, Body
from app.services.s3_service import S3Service
from app.services.openai_service import OpenAIService
from app.services.chat_service import ChatService
import uuid
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter()
s3_service = S3Service()
openai_service = OpenAIService()
chat_service = ChatService()

class ChatRequest(BaseModel):
    message: str
    game_state: Optional[Dict[str, Any]] = None

@router.post("/upload")
async def upload_poker_image(file: UploadFile = File(...)):
    try:
        # Read the file
        file_content = await file.read()
        
        # Generate unique filename
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"poker_hands/{str(uuid.uuid4())}.{file_extension}"
        
        # Upload to S3
        image_url = await s3_service.upload_file(file_content, unique_filename)
        
        # Analyze with OpenAI
        analysis_result = await openai_service.analyze_poker_image(image_url)
        
        return {"success": True, "data": json.loads(analysis_result)}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("")
async def chat(request: ChatRequest):
    try:
        response = await chat_service.get_response(request.message, request.game_state)
        return {
            "success": True,
            "data": {
                "message": response,
                "type": "bot"
            }
        }
    except Exception as e:
        print(f"Chat error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        } 
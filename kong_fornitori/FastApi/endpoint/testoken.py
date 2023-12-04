import os
import jwt
import datetime
from fastapi import APIRouter, Request, HTTPException

from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

@router.get("/testoken")
def getdisp(request: Request):
    """
    Testa la validità del token
    
    """
    token = request.headers.get('token')
    try:
        decode = jwt.decode(
            token, os.getenv('KEY'), algorithms=["HS256"]
        )
        return 'Token valido'
    except Exception:  
        return HTTPException(status_code=400, detail="Token errato o scaduto") 
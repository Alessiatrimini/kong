import os
import jwt
import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from Aclass.DataBaseExecuter import DataBaseExecuter as de
from config import mongoKong

load_dotenv()
router = APIRouter()

class Login(BaseModel):
    user: str
    psw: str

@router.post("/getoken")
def get_token(login: Login):
    """
    Restituisce il token da utilizzare nelle altre chiamate
    """
    mongodb_anafor = de(mongoKong['conn_str'], mongoKong['database'],  "users",  "", "mongo")
    utente = mongodb_anafor.selectbyqry({"user": login.user})
    if utente.empty:
        return HTTPException(status_code=500, detail="Username errato") 
    else:
        if utente.psw.iloc[0] == login.psw:
            encoded = jwt.encode({"exp": datetime.datetime.now() + datetime.timedelta(hours=1)},  os.getenv('KEY'), algorithm="HS256")
            token = encoded[:10] + str(utente.idazienda.iloc[0]) + encoded[10:]
            return token
        else:
            return HTTPException(status_code=500, detail="Password errata") 


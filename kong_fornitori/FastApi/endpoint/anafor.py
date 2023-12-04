import os
import jwt
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from IPython import embed
from fastapi import APIRouter, Request, HTTPException, Response
from Aclass.DataBaseExecuter import DataBaseExecuter as de
from config import mongoKong
load_dotenv()

class Filters(BaseModel):
    colname: str 
    value: str 
    operator : str

router = APIRouter()

@router.get("/anafor")
def anagrafica_fornitori(request: Request):
    """
    Restituisce i dati dell'anagrafica fornitore non sincronizzati sull'azienda, il parametro idazi è l'id identificativo dell'azienda.
    
    """
    token = request.headers.get('token')
    idazi = token[10]
    token = token[:10] + token[11:]
    try:
        decode = jwt.decode(
            token, os.getenv('KEY'), algorithms=["HS256"]
        )
    except Exception:  
        return HTTPException(status_code=400, detail="Token errato o scaduto") 
    

    mongodb_anafor = de(mongoKong['conn_str'], mongoKong['database'],  "anagrafica_fornitori",  "", "mongo")
    print(idazi)

    fornitori = mongodb_anafor.selectbyqry({"syncedon": {'$elemMatch': {'$ne' : int(idazi)}}})
    fornitori['_id']  = [str(i) for i in fornitori['_id']]
    
    return Response(content=json.dumps(fornitori.to_dict(orient = 'records')), media_type="application/json")


@router.post("/anafor/filter")
def anagrafica_fornitori_filtrata(request: Request, filter: Filters):
    """
    Restituisce i dati dell'anagrafica fornitore non sincronizzati sull'azienda.
    Chiave del body -> colname: nome della colonna su cui applicare il filtro, 
                        value: valore a destra dell'operatore, 
                        operator: operatore del filtro (valori validi per operator : $gte, $lte, $eq, $ne).
    
    """
    token = request.headers.get('token')
    token = token[:10] + token[11:]
    try:
        decode = jwt.decode(
            token, os.getenv('KEY'), algorithms=["HS256"]
        )
    except Exception:  
        return HTTPException(status_code=400, detail="Token errato o scaduto") 
    
    mongodb_anafor = de(mongoKong['conn_str'], mongoKong['database'],  "anagrafica_fornitori",  "", "mongo")
    fornitori = mongodb_anafor.selectbyqry({filter.colname: {filter.operator : filter.value}})
    if fornitori.empty:
        return [{}]
    else:
        fornitori['_id']  = [str(i) for i in fornitori['_id']]
        return Response(content=json.dumps(fornitori.to_dict(orient = 'records')), media_type="application/json")
 
    
@router.post("/anaforpartner/filter")
def anagrafica_per_partner_filtrata(request: Request, filter: Filters):
    """
    Restituisce i dati filtrati dell'anagrafica fornitore per singolo partner
    Chiave del body -> colname: nome della colonna su cui applicare il filtro, 
                        value: valore a destra dell'operatore, 
                        operator: operatore del filtro (valori validi per operator : $gte, $lte, $eq, $ne).
    """
    token = request.headers.get('token')
    token = token[:10] + token[11:]
    try:
        decode = jwt.decode(
            token, os.getenv('KEY'), algorithms=["HS256"]
        )
    except Exception:  
        return HTTPException(status_code=400, detail="Token errato o scaduto") 
    
    mongodb_anafor = de(mongoKong['conn_str'], mongoKong['database'],  "anafor_partner",  "", "mongo")
    fornitori = mongodb_anafor.selectbyqry({filter.colname: {filter.operator : filter.value}})
    if fornitori.empty:
        return [{}]
    else:
        fornitori['_id']  = [str(i) for i in fornitori['_id']]
        return Response(content=json.dumps(fornitori.to_dict(orient = 'records')), media_type="application/json")


@router.post("/anaforadd/filter")
def anagrafica_aggiuntiva_filtrata(request: Request, filter: Filters):
    """
    Restituisce i dati filtrati dell'anagrafica fornitore aggiuntiva (dati di performance)
    Chiave del body -> colname: nome della colonna su cui applicare il filtro, 
                        value: valore a destra dell'operatore, 
                        operator: operatore del filtro (valori validi per operator : $gte, $lte, $eq, $ne).
    """
    token = request.headers.get('token')
    token = token[:10] + token[11:]
    try:
        decode = jwt.decode(
            token, os.getenv('KEY'), algorithms=["HS256"]
        )
    except Exception:  
        return HTTPException(status_code=400, detail="Token errato o scaduto") 
    
    mongodb_anafor = de(mongoKong['conn_str'], mongoKong['database'],  "anafor_aggiuntiva",  "", "mongo")
    fornitori = mongodb_anafor.selectbyqry({filter.colname: {filter.operator : filter.value}})
    if fornitori.empty:
        return [{}]
    else:
        fornitori['_id']  = [str(i) for i in fornitori['_id']]
        return Response(content=json.dumps(fornitori.to_dict(orient = 'records')), media_type="application/json")
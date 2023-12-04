import os
import jwt
import json
from dotenv import load_dotenv
from IPython import embed
from fastapi import APIRouter, Request, HTTPException, Response
from pydantic import BaseModel

from Aclass.DataBaseExecuter import DataBaseExecuter as de
from config import mysqlKong

load_dotenv()
router = APIRouter()

class Modifier(BaseModel):
    colname: str 
    value: int 

class Modifier2(BaseModel):
    colname: str 
    value: str 

class ModifierCampi(BaseModel):
    insert :int
    field: str
    value: str 

@router.get("/partnerconfig")
def configurazione_partner(request: Request):
    """
    Restituisce i dati di configurazione dell'azienda
    
    """
    encode = request.headers.get('token')
    token = encode[:10] + encode[11:]
    idazi = encode[10]
    try:
        decode = jwt.decode(
            token, os.getenv('KEY'), algorithms=["HS256"]
        )
    except Exception:  
        return HTTPException(status_code=400, detail="Token errato o scaduto") 
    

    mysqldb = de(mysqlKong['host'], mysqlKong['database'],  mysqlKong['user'],  mysqlKong['password'], "mysql")
    qry_az = f"""select * from aziende_partner where idazienda = {idazi} """
    az_partner = mysqldb.selectbyqry(qry_az)

    return Response(content=json.dumps(az_partner.to_dict(orient = 'records')), media_type="application/json")

@router.post("/partnerconfig")
def configurazione_partner(request: Request, data: Modifier):
    """
    Permette di modificare il tipo di procedura (1 per automatica e due per REST API) ed il tipo di gestionale (1 per AS400 e 2 per SAP) 
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
    
    colqry = """select * from azienda_partner limit 1 """
    colname = mysqldb.selectbyqry(colqry).columns    
    
    if data.colname not in colname:
        return HTTPException(status_code=400, detail="Campo da assegnare errato")   
    if data.value not in [1, 2]:
        return HTTPException(status_code=400, detail="Valore da assegnare errato") 

    mysqldb = de(mysqlKong['host'], mysqlKong['database'],  mysqlKong['user'],  mysqlKong['password'], "mysql")
    qry = f"""UPDATE azienda_partner SET {data.colname} = {data.value} where idazienda = {idazi}"""
    mysqldb.executeqry(qry)

    return data
    
    
@router.get("/partnerconfig/erp")
def configurazione_partner_erp(request: Request):
    """
    Restituisce i dati di configurazione dell'erp dell'azienda
    """
    encode = request.headers.get('token')
    token = encode[:10] + encode[11:]
    idazi = encode[10]
    try:
        decode = jwt.decode(
            token, os.getenv('KEY'), algorithms=["HS256"]
        )
    except Exception:  
        return HTTPException(status_code=400, detail="Token errato o scaduto") 
    

    mysqldb = de(mysqlKong['host'], mysqlKong['database'],  mysqlKong['user'],  mysqlKong['password'], "mysql")
    qry_az = f"""select * from erpconn_partner where idazienda = {idazi} """
    az_partner = mysqldb.selectbyqry(qry_az)

    return Response(content=json.dumps(az_partner.to_dict(orient = 'records')), media_type="application/json")

@router.post("/partnerconfig/erp")
def configurazione_partner(request: Request, data: Modifier2):
    """
    Permette di modificare il tipo di procedura (1 per automatica e due per REST API) ed il tipo di gestionale (1 per AS400 e 2 per SAP) 
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
    mysqldb = de(mysqlKong['host'], mysqlKong['database'],  mysqlKong['user'],  mysqlKong['password'], "mysql")
    colqry = """select * from erpconn_partner limit 1 """
    colname = mysqldb.selectbyqry(colqry).columns

    if data.colname not in colname:
        return HTTPException(status_code=400, detail="Campo da assegnare errato")   

    qry = f"""UPDATE erpconn_paretner SET {data.colname} = {data.value} where idazienda = {idazi}"""
    mysqldb.executeqry(qry)

    return data

@router.get("/partnerconfig/campi")
def configurazione_partner_campi(request: Request):
    """
    Restituisce i dati di configurazione dei campi dell'azienda
    
    """
    encode = request.headers.get('token')
    token = encode[:10] + encode[11:]
    idazi = encode[10]
    try:
        decode = jwt.decode(
            token, os.getenv('KEY'), algorithms=["HS256"]
        )
    except Exception:  
        return HTTPException(status_code=400, detail="Token errato o scaduto") 
    
    mysqldb = de(mysqlKong['host'], mysqlKong['database'],  mysqlKong['user'],  mysqlKong['password'], "mysql")
    qry_az = f"""select * from asscampi_partner where idazienda = {idazi} """
    az_partner = mysqldb.selectbyqry(qry_az)

    return Response(content=json.dumps(az_partner.to_dict(orient = 'records')), media_type="application/json")

@router.post("/partnerconfig/campi")
def configurazione_partner_campi(request: Request, data: ModifierCampi):
    """
    Permette di modificare l'associazione dei campi; il parametro insert definisce se deve essere aggiunta una associazione (valore 1) o modificata una esistente (valore 1)
    
    """
    encode = request.headers.get('token')
    token = encode[:10] + encode[11:]
    idazi = encode[10]
    try:
        decode = jwt.decode(
            token, os.getenv('KEY'), algorithms=["HS256"]
        )
    except Exception:  
        return HTTPException(status_code=400, detail="Token errato o scaduto") 
    
    mysqldb = de(mysqlKong['host'], mysqlKong['database'],  mysqlKong['user'],  mysqlKong['password'], "mysql")

    colnqry = f"""select * from campiobl_fornitori where campo = '{data.field}' """
    colnamec = mysqldb.selectbyqry(colnqry)
    if colnamec.empty:
        return HTTPException(status_code=400, detail="Campo da assegnare errato") 
    
    if data.insert == 1:   
        qry = f"""INSERT INTO asscampi_partner (idazienda, idcampo, label_campo) values ({idazi}, {colnamec.idcampo.iloc[0]}, '{data.value}')"""
        mysqldb.executeqry(qry)

    elif data.insert == 0:  
 
        qry = f"""UPDATE asscampi_partner SET label_campo = '{data.value}' where idazienda = {idazi} and idcampo = {colnamec.idcampo.iloc[0]}"""
        mysqldb.executeqry(qry)
    else:
        return HTTPException(status_code=400, detail="Valore del parametro insert errato")  
    return data
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from endpoint import anafor, getoken, partnerconfig
load_dotenv()

from IPython import embed
from config import origins

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(anafor.router)
app.include_router(getoken.router)
app.include_router(partnerconfig.router)


@app.get("/")
def health_server():
    """
    Verifica se l'api è online
    """
    return "KONG API ONLINE"

if __name__ == '__main__':
    
    uvicorn.run(
        'main:app', 
        port = 50400, 
        host = '0.0.0.0',
        reload = True,
        ssl_keyfile = os.getenv("PRIVKEY"),
        ssl_certfile= os.getenv("CERT")
        )
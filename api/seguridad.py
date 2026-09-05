from dotenv import load_dotenv
import os
from fastapi import Header, HTTPException, Depends



load_dotenv()
API_KEY = os.environ["API_KEY"]

def verificar_clave(x_api_key: str= Header()):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="La contraseña de entrada no es correcta")
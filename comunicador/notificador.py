from dotenv import load_dotenv
import os
import httpx

load_dotenv()
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def enviar(mensaje:str) -> None:

    return httpx.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})
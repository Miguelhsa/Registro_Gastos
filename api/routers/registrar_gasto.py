from fastapi import APIRouter
from pydantic import BaseModel
from dominio.modelos import Gasto
from datetime import date
from persistencia.repositorio import guardar
from comunicador.notificador import enviar

class GastoIn(BaseModel):
    categoria: str
    importe: float


router = APIRouter(prefix="/registrar", tags=["registro_gasto"])

@router.post("")
def registrar(entrada:GastoIn):
    #recibo un str y un float y tengo que reconstruir un Gasto
    gasto_entrada = Gasto(date.today(),entrada.categoria,entrada.importe)
    #el objetoi creado (Gasto) se lo paso a guardar
    guardar(gasto_entrada)
    #enviar un mensaje de que todo esta correcto
    enviar(f"gasto con fecha {gasto_entrada.fecha}, en {gasto_entrada.categoria} una cantidad de {gasto_entrada.importe} introducido correctamente")
    #mensaje paa el usuario
    return {"ok": True}
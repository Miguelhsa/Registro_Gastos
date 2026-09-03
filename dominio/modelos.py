#Aqui se hacen los cáculos que entran.
from dataclasses import dataclass
from datetime import date

#como es el objeto gasto
@dataclass
class Gasto:
    fecha: date
    categoria: str
    importe: float

#Para calcular los gastos de hoy tengo que repasar todas las lineas e ir acumulando el gasto
def gastos_hoy(gastos: list[Gasto]) -> float:
    total = 0
    for linea in gastos:
        if linea.fecha == date.today():
            total += linea.importe

    return total

#Aqui estarán las funciones de guardar y cargar que conectarán con Google sheets
#from dominio.modelos import Gasto
#import json 
#from dataclasses import asdict
#from datetime import date

import gspread
from dominio.modelos import Gasto
from datetime import date
"""
#guardar: objeto → dict → texto → archivo
def guardar(gasto:Gasto) -> None:
    with open ("gastos.json", "a") as gastos:
        gasto_guardar = asdict(gasto) #convierto el objeto en un json
        gasto_guardar["fecha"] = gasto_guardar["fecha"].isoformat()#hay que cambiar el formato ya uqe jsondumps no sabe leer bie
        gasto_guardar_str = json.dumps(gasto_guardar) #Convierto el json en un str
        gastos.write(gasto_guardar_str + "\n")

#cargar: archivo → texto → dict → objeto
#Recordar que no hace ninguna operacion, solo entrega la lista complea
def cargar() -> list[Gasto]:
    lista_gastos = []
    with open("gastos.json", "r") as gastos:
        for linea in gastos:
            #linea es un str - convertirla a un dict
            gasto = json.loads(linea)
            #convertir la fecha en un formato legible
            gasto["fecha"] = date.fromisoformat(gasto["fecha"])
            #convertir ese json a objeto
            gasto_unidad = Gasto(gasto["fecha"],gasto["categoria"],gasto["importe"])
            lista_gastos.append(gasto_unidad)

    return lista_gastos
    """

# Conexión: el robot inicia sesión con sus credenciales y abre la hoja
gc = gspread.service_account(filename="credenciales.json")
hoja = gc.open("Control-gastos").sheet1   # abre la hoja por su nombre y coge la 1ª pestaña

def guardar(gasto:Gasto) -> None:
    hoja.append_row([gasto.fecha.isoformat(),gasto.categoria,gasto.importe])

def cargar() -> list[Gasto]:
    lista_gastos = []
    lista = hoja.get_all_values(value_render_option="UNFORMATTED_VALUE")
    for gastos in lista:
        obj_gasto = Gasto(date.fromisoformat(gastos[0]),gastos[1],float(gastos[2]))
        lista_gastos.append(obj_gasto)
    return lista_gastos
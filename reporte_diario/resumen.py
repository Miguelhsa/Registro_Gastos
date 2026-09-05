from persistencia.repositorio import guardar, cargar
from dominio.modelos import gastos_hoy
from comunicador.notificador import enviar


#Pide a persistencia, dominio y comunicador su parte y las enlaza 

#1 carga la lista de gastos
#2 Hace el total de los gastos
#3 Redacta el mensaje 
#4 envia el mensaje al comunicador

 
def enviar_resumen() -> None:
    #cargo lo gastos -> list[Gastos]
    lista_gastos = cargar()
    #calculo los gastos totales de hoy -> float
    gastos_totales = gastos_hoy(lista_gastos)
    #Redacta el mensaje -> str
    mensaje = f"Los gastos de hoy han sido {gastos_totales}"
    #Enviar el mensaje a funcion enviar 
    return enviar(mensaje)
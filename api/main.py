from fastapi import FastAPI
from api.routers.salud import router as router_salud
from api.routers.registrar_gasto import router as registro_gasto
from api.seguridad import verificar_clave


app = FastAPI()
app.include_router(router_salud)
app.include_router(registro_gasto)


    

#Para levantar el servidor 
# uv run fastapi dev api/main.py
# similar a uvicorn, corre por debajo
# Tiene el reload implicito
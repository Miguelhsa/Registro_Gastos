# PROGRESO — control-gastos

Bitácora de dónde lo dejamos cada sesión. Se empieza leyendo esto + el README (mapa vivo).

## Estado general
Backend completo y probado de punta a punta, en master:
registrar gasto por Streamlit -> API (valida + auth por clave) -> Dominio -> Persistencia (gastos.json) -> Comunicador (Telegram real al móvil). Los dos flujos vivos.

Ahora estamos en la **Fase 6: empaquetar en Docker**.

## Sesión de hoy (2026-09-08) — Docker, paso 2 hecho
Plan de Docker en pasos pequeños:
  1. Entender qué es una caja (imagen vs contenedor vs Dockerfile).  [HECHO]
  2. Escribir la receta de la API: el Dockerfile, línea a línea.      [HECHO]
  3. Construir la caja y arrancarla.                                  [<- AQUÍ SEGUIMOS MAÑANA]

Escritos y comentados (aún SIN commitear — pendiente tu flujo rama->PR):
- `Dockerfile` (raíz): FROM python:3.14-slim / WORKDIR /app / COPY . . /
  RUN pip install uv / RUN uv sync --no-dev / EXPOSE 8000 /
  CMD ["uv","run","fastapi","run","api/main.py","--port","8000"].
  Cada línea lleva su comentario explicativo. Corregido un bloque """...""" (sintaxis Python)
  que habría roto la construcción: en Dockerfile solo vale # como comentario.
- `.dockerignore` (raíz): deja fuera .env (SECRETOS), .venv, .git, __pycache__, *.pyc,
  gastos.json, .streamlit. Comentado. Aprendido: en .dockerignore el # solo es comentario
  al PRINCIPIO de línea (a mitad de línea se pega al patrón y lo estropea).

## Próximos pasos (en orden)
1. PASO 3 — construir la imagen de la API (`docker build`) y arrancarla (`docker run`), comprobar
   que responde (/salud, /docs). Ver por qué hace falta pasarle el .env al arrancar (los secretos
   NO están dentro de la imagen, y bien: van al encender el contenedor, no horneados).
2. Dockerfile del **front** (Streamlit).
3. **docker-compose** para conectar los dos contenedores: cambiar en el front la URL
   `http://127.0.0.1:8000` -> `http://api:8000` (se llaman por NOMBRE de servicio en la red de Docker).

## Recordatorio de método
Mentor: guío con preguntas/pistas; el código Python lo escribe Miguel. Dockerfile/config los puedo
dar yo con su porqué. Una pieza cada vez; el "para qué" antes del detalle.

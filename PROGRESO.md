# PROGRESO — control-gastos

Bitácora de dónde lo dejamos cada sesión. Se empieza leyendo esto + el README (mapa vivo).

## Estado general
Proyecto completo y probado de punta a punta, y AHORA CORRIENDO EN DOCKER:
registrar gasto por Streamlit -> API (valida + auth por clave) -> Dominio -> Persistencia (gastos.json) -> Comunicador (Telegram real al móvil). Los dos flujos vivos.

**Fase 6 (empaquetar en Docker): TERMINADA.** ✅

## Sesión 2026-09-12 — Docker cerrado
Se completó todo el empaquetado y funciona end-to-end (gasto por el front -> Telegram):

- `Dockerfile.api` (antes `Dockerfile`, renombrado): receta de la API. FROM python:3.14-slim,
  WORKDIR /app, COPY . ., pip install uv, uv sync --no-dev, EXPOSE 8000,
  CMD uv run fastapi run api/main.py. Comentado línea a línea.
- `Dockerfile.frontend`: receta del front. Igual que la API salvo 3 cosas:
  uv sync --no-dev --group frontend (trae Streamlit), EXPOSE 8501,
  CMD uv run streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true.
- `.dockerignore`: deja fuera .env (secretos), .venv, .git, __pycache__, *.pyc, gastos.json, .streamlit.
- `docker-compose.yml`: dos servicios (api, front). api con env_file: .env y ports 8000:8000;
  front con ports 8501:8501 y depends_on api. Compose monta una red común donde cada servicio
  es alcanzable por su NOMBRE.
- Cambio en `frontend/app.py` (línea 20): la URL pasó de http://127.0.0.1:8000 a http://api:8000
  (el front llama a la API por su NOMBRE de servicio, por la red interna de Docker).
- pyproject.toml: streamlit movido a [dependency-groups] frontend (la API ya no lo instala ->
  imagen de 800MB a 400MB).

Conceptos aprendidos hoy:
- Separar dependencias por grupos (uv --group) = responsabilidad única también en las imágenes.
- Puertos: "8000/tcp" (solo interno) vs "0.0.0.0:8000->8000" (publicado al Mac). Publicar puertos
  es para que TÚ entres desde el Mac; para que caja hable con caja basta la red interna + el nombre.
- Bug resuelto: contenedores viejos que no compartían red -> "Name or service not known".
  Se arregla con `docker compose down` + `docker compose up --build` (borrón y cuenta nueva).
- Para probar dentro de una caja hay que usar `uv run python`, no `python` pelado (las libs viven en /app/.venv).

Arrancar todo:  docker compose up --build   (parar/limpiar: docker compose down)

## Cabos sueltos / próximos pasos (Miguel elige orden; recomendado 1 primero)
1. **Cerrar git**: TODO el trabajo de Docker sigue SIN commitear. Flujo rama->PR->merge.
   (Recordar: `frontend/*.jpg` va en .gitignore; NO subir la foto personal. Repo público.)
2. **Volúmenes**: los gastos se guardan DENTRO de la caja y se BORRAN al recrear. Falta un
   volumen de Docker para que gastos.json sobreviva.
3. **Resumen diario automático (CRON JOB)**: el código existe (reporte_diario/enviar_resumen)
   pero nadie lo dispara cada día. Falta montar el mecanismo (2º orquestador).
4. (Evolución) cambiar el almacén JSON por Google Sheets.

## Recordatorio de método
Mentor: guío con preguntas/pistas; el código Python lo escribe Miguel. Dockerfile/config los puedo
dar yo con su porqué. Una pieza cada vez; el "para qué" antes del detalle. Ir retirando ruedas.

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

## Sesion 2026-09-13 (tarde) - Volumen + Cron cerrados
- **Volumen (cabo 2) HECHO**: en docker-compose, servicio api lleva
  `volumes: - ./gastos.json:/app/gastos.json` (bind mount). Los gastos ya sobreviven a down/up.
  Concepto: imagen/contenedor/volumen son 3 cosas independientes; borrar imagen NO borra datos.
  Bind mount = un PUENTE a un archivo que ya existe en el Mac (sin almacen propio); named volume =
  cajon gestionado por Docker. Publicar puertos es para que TU entres; datos y secretos NO viajan
  con el compose (son de cada maquina), igual que el .env.
- **Cron / resumen diario (cabo 3) HECHO**: tercer contenedor dedicado.
  - `pyproject.toml`: nuevo grupo [dependency-groups] cron = apscheduler.
  - `reporte_diario/planificador.py` (NUEVO): BlockingScheduler(timezone="Europe/Madrid"),
    add_job(enviar_resumen, "cron", hour=22, minute=0), .start(). (linea interval, minutes=1 comentada para pruebas).
  - `Dockerfile.cron` (NUEVO): como la API pero uv sync --group cron, SIN EXPOSE (nadie se conecta A el),
    CMD uv run python -m reporte_diario.planificador (el -m es clave para que los imports absolutos funcionen).
  - `docker-compose.yml`: servicio cron con env_file .env y el MISMO volumen de gastos.json
    (la API escribe, el cron lee). Sin ports ni depends_on (el cron NO pasa por la API; usa las capas directamente).
  - Probado con interval minutes=1 (Telegram cada minuto), luego cambiado a cron diario 22:00.
- **Git HECHO**: PR #3 (docker) y PR #4 (cron-volumen) mergeados en master. Todo commiteado.
- Conceptos: BlockingScheduler = llamada SINCRONA/bloqueante que no vuelve nunca -> mantiene vivo el
  proceso -> mantiene viva la caja (pero un `docker compose down` la para igual: el control externo es tuyo).
  interval (cada X tiempo) vs cron (momento del reloj). Pasar la funcion sin () a add_job.

## Cabos sueltos
1. Cerrar git — HECHO.
2. Volumen — HECHO.
3. Resumen diario / cron — HECHO.
4. **Google Sheets — PENDIENTE (aqui seguimos manana).**

### Plan de Google Sheets (cabo 4)
LA RECOMPENSA de la arquitectura: para pasar de JSON a Sheets se cambia UN SOLO archivo,
`persistencia/repositorio.py`. Dominio, API, Comunicador, cron y front NO se tocan (siguen llamando
guardar()/cargar() igual). Es el pago del patron repositorio.

Dos mitades:
- **Mitad A (fontaneria)**: (1) libreria `gspread`, (2) credenciales = una CUENTA DE SERVICIO de
  Google Cloud que da un JSON, (3) COMPARTIR la hoja de Sheets con el email de esa cuenta de servicio.
  El JSON de credenciales es un SECRETO -> fuera de la imagen, fuera de git, inyectado como el .env.
  (gspread ira en su propio grupo de dependencias, p. ej. group sheets.)
- **Mitad B (codigo, lo escribe Miguel)**: reescribir guardar()/cargar() en repositorio.py para que
  escriban una fila / lean las filas de la hoja, en vez del archivo json.

Preguntas abiertas para arrancar manana:
  1) Tiene ya una hoja de Google Sheets creada, o la creamos?
  2) Ha tocado antes la consola de Google Cloud (proyecto, cuenta de servicio), o es terreno nuevo?


## Recordatorio de método
Mentor: guío con preguntas/pistas; el código Python lo escribe Miguel. Dockerfile/config los puedo
dar yo con su porqué. Una pieza cada vez; el "para qué" antes del detalle. Ir retirando ruedas.

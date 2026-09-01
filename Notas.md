# 1. Proyecto uv (declara el proyecto y, luego, sus dependencias)
uv init --bare
#    Si tu uv no conoce --bare: usa `uv init` y borra el main.py/hello.py de ejemplo que cree.

# 2. Git + qué NO subir
git init
#    Crea el .gitignore tú, con al menos:  .venv/   __pycache__/   .env   *.pyc
#    (el .env va sí o sí: ahí vivirá la clave de la API de la que hablamos)

# 3. Primer commit del esqueleto
git add -A
git commit -m "Estructura inicial de control-gastos (capas + pyproject)"

# 4. Rama para el trabajo del dominio (flujo rama→PR desde el minuto uno)
git switch -c dominio
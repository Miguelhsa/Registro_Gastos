# 1. Proyecto uv (declara el proyecto y, luego, sus dependencias)
uv init --bare
#    Si tu uv no conoce --bare: usa `uv init` y borra el main.py/hello.py de ejemplo que cree.

uv init convierte la carpeta actual en un proyecto gestionado por uv. Su acto central es crear un pyproject.toml: el manifiesto del proyecto —su nombre, qué versión de Python necesita y, según las vayas añadiendo, sus dependencias declaradas (el concepto que ya tienes: las dependencias se declaran en un archivo, no se instalan a mano y a ver qué queda). Más adelante, cuando hagas uv add fastapi, la línea se escribe ahí.

Por defecto, además del pyproject.toml, uv init te monta andamiaje de cortesía: un main.py de ejemplo, un .python-version, un README.md, y hasta te inicia un repo git con su .gitignore.

--bare significa "pelado": crea solo el pyproject.toml y se salta todo ese andamiaje —ni archivo de ejemplo, ni README, ni git.

Por eso te lo propuse a ti: ya tienes tu README, tu estructura de carpetas y quieres hacer el git tú (es tu re-práctica de Fase 0). El andamiaje solo pisaría lo que ya construiste. Con --bare te llevas el manifiesto limpio y nada más.

Un matiz importante: uv init no crea todavía el entorno (.venv) ni instala nada. Ese entorno —la carpeta aislada que ya conoces— aparece solo cuando haga falta, con el primer uv add o uv run.
# 2. Git + qué NO subir
git init
#    Crea el .gitignore tú, con al menos:  .venv/   __pycache__/   .env   *.pyc
#    (el .env va sí o sí: ahí vivirá la clave de la API de la que hablamos)

# 3. Primer commit del esqueleto
git add -A
git commit -m "Estructura inicial de control-gastos (capas + pyproject)"

# 4. Rama para el trabajo del dominio (flujo rama→PR desde el minuto uno)
git switch -c dominio
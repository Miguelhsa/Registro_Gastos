# --- imports: la clase del reloj y tu función del resumen ---
from apscheduler.schedulers.blocking import    BlockingScheduler   # (1)
from reporte_diario.resumen import enviar_resumen          # (2)

# --- crea el reloj ---
scheduler = BlockingScheduler(timezone="Europe/Madrid")                                   # (3)

# --- registra el trabajo: qué función, tipo de horario, y a qué hora ---
scheduler.add_job(enviar_resumen, "cron", hour=22, minute=0)  # (4)
#scheduler.add_job(enviar_resumen, "interval", minutes=1) #este funciona por intervalos

# --- arráncalo (esto BLOQUEA -> mantiene la caja viva) ---
scheduler.start()                                     # (5)
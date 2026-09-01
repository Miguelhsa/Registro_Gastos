<!-- Mapa vivo del proyecto. Lo alimentamos a lo largo del proyecto. Se empieza cada sesión por aquí.
     Orden macro: propósito → capacidades → capas → carpetas → qué entrega/quién consume;
     el modelo de dominio (los objetos) se rellena DESPUÉS. -->

# Control de Gastos

## Qué es / propósito

Un registro de mis gastos: cada vez que tengo un gasto, apunto una línea y queda guardada.
Sirve para tener el control de en qué se va el dinero sin revisarlo a mano — el programa me lo
comunica solo: un aviso al momento por cada gasto nuevo y un resumen diario automático.

## Qué hace (capacidades)

1. Registrar un gasto — apuntar una línea con sus datos y que quede guardada.
2. Avisar al momento cada vez que se registra un gasto.
3. Enviar un resumen diario automático de los gastos.

<!-- Aquí solo el QUÉ. El CÓMO de cada capacidad (dónde se guarda, por qué canal avisa) es
     capas/adaptadores y se decide en el diseño macro. Ideas de partida (a validar): guardar en
     Google Sheets; avisar por Telegram. -->

## Capas (arquitectura macro)

Seis piezas + dos sistemas externos. Diseñada por Miguel (sesión 42).

**Obreros (el núcleo, hacen el trabajo):**
- **Dominio** — modela el gasto y hace los cálculos (p. ej. el resumen del día natural: los gastos de hoy, 00:00–23:59).
  PROHIBIDO: guardar, enviar o saber que existen FastAPI / Google Sheets / Telegram.
  **No depende de nadie** (regla de oro): todos pueden apoyarse en él, él no llama a nadie.
- **Persistencia (repositorio)** — ÚNICO que lee y escribe en el almacén. Esconde que el almacén
  es Google Sheets. PROHIBIDO: calcular o notificar.
- **Comunicador Telegram (notificador)** — adaptador de SALIDA; ÚNICO que habla con Telegram.
  Lo usan los dos flujos. PROHIBIDO: calcular o guardar.

**Orquestadores (coordinan, no hacen el trabajo):**
- **API** — interfaz de ENTRADA. Recibe el gasto del usuario, coordina el flujo de registro
  (dominio → persistencia → comunicador) y responde al usuario. No sabe cómo se guarda ni cómo se envía.
- **CRON JOB (disparador diario)** — orquestador del flujo diario. Una vez al día dispara: pide datos a la
  Persistencia → el cálculo al Dominio → el envío al Comunicador. No hace ninguno de esos trabajos; los coordina.

**Sistemas externos (pasivos, en el borde):**
- **Google Sheets** — almacén; solo guarda.
- **Telegram** — mensajería; solo recibe el aviso.

**Flujos y dirección de dependencias:**
- Flujo 1 (registrar gasto): Usuario → API → { Dominio, Persistencia, Comunicador }. Persistencia → Google Sheets. Comunicador → Telegram.
- Flujo 2 (resumen diario): CRON JOB → Persistencia (leer) → Dominio (calcular) → Comunicador (enviar) → Telegram.
- Regla de oro: el **Dominio no depende de nadie**. Solo la **Persistencia** toca Google Sheets; solo el **Comunicador** toca Telegram.
- Simetría clave: **dos orquestadores** (API, CRON JOB) sobre **tres obreros** (Dominio, Persistencia, Comunicador). A uno lo dispara el usuario, al otro un reloj.

## Carpetas

<!-- PENDIENTE — lo razonas TÚ, después de las capas. -->

## Qué entrega y quién lo consume

<!-- PENDIENTE. -->

## Modelo de dominio (los objetos)

<!-- LO MICRO: PENDIENTE, después de la macro. -->

# Resumen y mapa de pantallas

## Del CDC a las pantallas
El CDC de HeraHub suele estructurarse por **processus/modules** en orden de prioridad, cada uno con «Ce que nous avons compris», «Ce que nous allons développer» (lista numerada 1.1, 1.2…), «Pour qui», «Tâches couvertes» y «Points à confirmer». Úsalo así:

- **Módulo de la demo = processus del CDC**, en el mismo orden. El nombre se acorta a 1-2 palabras del oficio («Commercial», «Appels d'offres», «Production»).
- **Pantalla = desarrollo concreto** de «Ce que nous allons développer», agrupando los que comparten objeto. 2-5 pantallas por módulo; si salen más, fusiona.
- **Perfil = «Pour qui»**: cada pantalla tiene una persona principal, que es el perfil desde el que se enseña.
- Las tareas con más horas/mes y nota 5/5 tienen que verse en la demo: son el argumento comercial.
- **Accueil** siempre: KPIs y listas «à traiter aujourd'hui» que vienen de los módulos.
- Si el alcance es reducido, elige los módulos de mayor prioridad y, dentro de ellos, las pantallas que ataquen las tareas más pesadas.

## Elegir la forma de cada pantalla
La pregunta es: **¿cómo hace hoy esta persona esta tarea, y qué forma tiene ese trabajo?** No empieces por «una tabla con filtros».
| Si el trabajo es… | Forma |
|---|---|
| hacer avanzar cosas por etapas (devis, pedidos, expedientes) | kanban con importes y responsables |
| revisar y actuar sobre muchas líneas (facturas, stock, contactos) | tabla densa + filtros chip + cajón de detalle |
| una cola de acciones del día (relances, llamadas, alertas) | lista priorizada con acciones en línea (llamar, enviar) |
| producir en taller o en obra, con guantes o tablet | pantalla completa oscura (`base_bare`), botones enormes, una sola orden a la vista |
| planificar en el tiempo (citas, rondas, publicaciones, salones) | calendario o línea temporal |
| analizar un documento (CCTP, contrato, pedido) | zona de carga + resultado extraído editable + «Synchronisé avec <herramienta>» |
| seguir algo que se mueve (envíos, intervenciones) | frise/timeline + estado + mapa sencillo |
| configurar reglas (relances automáticas, umbrales) | lista de reglas legibles («J+7 sans réponse → e-mail») con interruptores |
| comparar ofertas o proveedores | tabla comparativa con la mejor opción marcada |
Cada pantalla tiene **una acción principal** (el único `.btn-primary`) y varias secundarias.

**CRUD siempre en modales.** Cualquier entidad que el usuario crea, modifica o borra (clientes, pedidos, artículos, contactos, reglas…) es UNA pantalla de listado con crear / editar / eliminar en modales y detalle en cajón lateral, nunca páginas aparte de «nuevo» o «editar». En el mapa de pantallas, marca la forma como «listado + CRUD en modales». El listado puede ser tabla, kanban o tarjetas según el trabajo; las modales son las mismas.

Si el cliente usa una herramienta que se queda (ej. Interfast, Sellsy, Sage), la demo **no la sustituye**: muestra la integración (badge «Synchronisé avec X», botón «Envoyer vers X»).

## Formato de `documentos/RESUMEN_ES.md`
```markdown
# <Cliente> · resumen para el equipo
Fuente: CDC v<N> (<estado>) + <otros documentos>. Equipo Koralya: <trabajadores_asignados>.

## El cliente
<5 líneas: qué hace, tamaño, cómo trabaja hoy, herramientas principales>

## Problemas principales
- <problema concreto con cifra: «el responsable de licitaciones pasa ~2 h/semana leyendo pliegos de 110 páginas»>
(5-8 puntos, ordenados por peso en el CDC)

## Lo que se ha prometido
<módulos del CDC en orden de prioridad, una línea cada uno con el gain estimado>

## Qué tienes que leer tú
1. `<ruta>`: <por qué, en una línea>
(3-5 documentos como mucho, con la traducción si existe)

## Puntos abiertos del CDC
<«Points à confirmer» que afectan a la demo, y qué supuesto toma la demo>

## Demo propuesta
Idioma: <idioma> · Identidad: <colores, tipografías, forma; de dónde salen>
| Módulo | Pantalla | Forma | Perfil | Por qué |
|---|---|---|---|---|
| Commercial | Pipeline | kanban por etapa con importes | Dirección comercial | conversión invisible hoy (classeurs) |
…
```
En el chat, muestra el resumen entero o casi, y pregunta: «¿Construyo este mapa de pantallas o cambias algo?»

## `plan.json`
Lo escribes tú a partir del mapa validado (formato en el docstring de `scripts/scaffold.py`). `screens[].url` en minúsculas, con guiones y en el idioma de la app (`appels-offres/veille/`). `icon` = nombre Lucide (https://lucide.dev/icons). Usa un `section` para separar módulos secundarios (ej. «Visibilité»).

# Traducciones al español

El equipo lee en español y los documentos del cliente suelen estar en francés. Traducir es parte del trabajo, no un extra: hazlo siempre, en segundo plano, sin que bloquee la demo.

## Qué se traduce
Cada documento en otro idioma que no sea el español y que describa el proyecto:
- CDC (`cahier_des_charges.md`) → `cahier_des_charges_ES.md`
- Recomendaciones → `recommandations_ES.md`
- Carta gráfica (texto de la guía + LISEZ-MOI) → `charte_graphique_ES.md`
- **Cada** transcripción de entrevista → `transcripcion_<Nombre>_ES.md`
- Síntesis, auditorías en PDF y documentos de proceso relevantes → `<nombre>_ES.md`

No se traducen: CSV/JSON de datos (se leen tal cual), facturas, Excels de cifras. Si el documento ya está en español, no se traduce.

## Cómo
Un subagente por documento, todos lanzados en el mismo mensaje con `run_in_background` (los resultados llegan solos; no esperes ni hagas polling). Los documentos largos (>60k caracteres) se dividen en partes de unos 40k, cortando en un salto de sección o en una marca de tiempo, y cada parte la traduce un subagente. Al final se concatenan en orden.

Brief para cada subagente (rellena los <…>):

```
Traduce al español de España el archivo <ruta origen> y guarda el resultado en <ruta destino>.

Reglas:
- Traducción ÍNTEGRA y fiel, no un resumen: mismo orden, mismas secciones, mismas tablas,
  mismas marcas de tiempo. El lector la usará en lugar del original.
- Mantén el formato Markdown (títulos, listas, tablas, negritas).
- No traduzcas: nombres de personas y empresas, nombres de herramientas (Interfast, Sellsy…),
  referencias, siglas del oficio (CCTP, DPGF, OA, HTA…) ni cifras. La primera vez que aparezca
  una sigla poco obvia, añade entre corchetes su sentido: «CCTP [pliego de prescripciones técnicas]».
- Transcripciones orales: conserva el tono hablado y las repeticiones; si un pasaje es
  ininteligible o dudoso en el original, márcalo con [?].
- Empieza el archivo con esta línea y una línea en blanco:
  > Traducción al español de «<nombre del original>». Uso interno. [?] = pasaje dudoso en el original.
- Si el archivo es muy largo, trabaja por bloques (lee una parte, traduce, añade al archivo
  de destino) hasta terminarlo entero. No te saltes partes.
- Al acabar, responde solo con: ruta escrita y número aproximado de líneas.
```

## Comprobación
Antes de entregar, confirma que existe cada archivo `_ES.md` esperado y que su longitud es parecida a la del original (entre el 80 y el 130 %). Si uno es mucho más corto, se resumió en vez de traducirse: relánzalo.

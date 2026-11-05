# Identidad visual del cliente

La demo lleva **la marca del cliente**. HeraHub solo aparece con un discreto «Développé par HeraHub» en la pantalla de login (ya está en la base).

Toda la identidad cabe en el bloque `identity` de `plan.json`, que `scripts/tokens.py` convierte en `tokens.css`:

```json
"identity": {"brand": "#F07D00", "ink": "#1E1D1D", "accent": null,
             "font_title": "Poppins", "font_body": "Montserrat",
             "shape": "pill", "sidebar": "dark"}
```
- `brand`: color principal. Se genera la gama 50→900 y el color de texto sobre la marca (blanco o anthracite) según el contraste WCAG. Por ejemplo, sobre naranja el texto queda oscuro, como manda la carta de nuestra demo de referencia.
- `ink`: neutro más oscuro (opcional). Por defecto es un anthracite ligeramente teñido de la marca.
- `accent`: segundo color (opcional) para gráficos y badges `.accent`. Nunca para un segundo botón principal.
- `font_title` / `font_body`: Google Fonts.
- `shape`: `pill` (botones cápsula) · `soft` (radio 10 px) · `sharp` (radio 4 px).
- `sidebar`: `dark` · `light` · `brand`.

## Caso A · Hay carta gráfica
Se aplica **tal cual**, sin reinterpretarla:
- Si trae tokens (`tokens.css`, `tailwind.config.js`), copia sus valores a `core/static/css/tokens.css` respetando los **nombres de variable de la base** (`--brand-*`, `--ink-*`, `--on-brand`, `--radius-*`, `--font-*`…): app.css depende de ellos. Ejecuta antes `tokens.py` para tener el archivo completo y sustituye después los valores que da la carta.
- Copia sus «reglas que no se pueden romper» en `DESIGN_GUIDE.md` § Reglas innegociables.
- Logos, iconos y capturas de la carta → `core/static/img/`. El símbolo, en SVG `currentColor`, va a `partials/mark.html`.

## Caso B · No hay carta gráfica → pregunta
Una sola pregunta con AskUserQuestion: «No hay carta gráfica para <cliente>. ¿De dónde saco los colores?»
1. **Web del cliente**: el usuario da la URL (o la buscas tú y la confirma).
2. **Me digo los colores**: con palabras está bien («naranja», «azul marino», «mezcla de naranja y azul»). No hacen falta hexadecimales.
3. **Que decida la skill**: tú eliges lo más bonito y adecuado.

### 1 · Desde la web
- Ábrela con WebFetch (o Claude in Chrome si el contenido se carga con JS) y extrae:
  - Colores: variables CSS (`--primary`, `--color-*`), color de botones y enlaces, cabecera y pie. Quédate con 1 principal y, si existe, 1 secundario. Ignora negros, blancos y grises puros.
  - Tipografías: `font-family` de títulos y texto. Si son de Google Fonts, úsalas. Si son de pago, busca la equivalente más cercana en Google Fonts y dilo.
  - Logo: el `<img>`/`<svg>` de la cabecera o el favicon. Descárgalo a `core/static/img/` y redibuja el símbolo en SVG `currentColor` para `partials/mark.html`.
  - Forma: si los botones de su web son cápsula → `pill`; si son rectos → `sharp`.
- Si la web es pobre o anticuada, toma solo el color y el logo, y aplica el criterio del caso 3 para lo demás.

### 2 · Colores dichos con palabras
Tradúcelos a hex con criterio de diseñador, no de paleta básica. Evita los primarios puros (#FF0000, #0000FF): ajusta la saturación para pantalla y para que quepa texto encima.
| Dicho | Punto de partida |
|---|---|
| naranja | #F07D00 |
| rojo | #D63B2F (más vivo) · #B3261E (más sobrio) |
| azul / azul corporativo | #1F5FAD |
| azul marino | #1F3A5F |
| verde | #2E7D4F |
| verde agua / turquesa | #11847E |
| amarillo | #F2B705 (el texto encima queda oscuro, es automático) |
| morado / violeta | #6B3FA0 |
| burdeos | #7A1F3D |
| gris / antracita | brand = un tono vivo del sector; `ink` = #2B2B2E |
«Mezcla de A y B» → la que domine será `brand` y la otra `accent`. Si no está claro cuál domina, el más saturado va de `brand` y el oscuro de `accent`.

### 3 · Lo decide la skill
Decide a partir del logo (si existe en los documentos) y del sector. Justifica la elección en una línea en el resumen.
- Industria, construcción, energía: colores con cuerpo (naranja, azul acero, verde industrial), `sidebar: dark`, `shape: soft`.
- Salud, bienestar, formación: verdes o azules suaves, `sidebar: light`, `shape: pill`.
- Servicios financieros, jurídicos, consultoría: azul marino o verde botella, `sidebar: brand` o `dark`, `shape: sharp`.
- Comercio, moda, cultura: un color con personalidad (terracota, ciruela, mostaza) y una tipografía de títulos con carácter.

Parejas tipográficas que funcionan (títulos / texto): Poppins / Montserrat · Space Grotesk / Inter Tight · Manrope / Manrope · Plus Jakarta Sans / Plus Jakarta Sans · Sora / Nunito Sans · DM Sans / DM Sans · Outfit / Source Sans 3 · Fraunces / Inter Tight (más editorial).

## Lo que delata a una IA (evítalo siempre)
- Degradado índigo/violeta, «glassmorphism», texto con degradado, sombras de colores en todo.
- Inter + azul #3B82F6 por defecto «porque sí».
- Emojis en la interfaz, iconos dentro de círculos de colores en cada tarjeta.
- Hero con frase grande y subtítulo dentro de una herramienta interna.
- Todo en tarjetas idénticas con el mismo radio y la misma sombra.
- Color de marca por todas partes: debe quedar por debajo del ~5 % de la pantalla (un botón principal por zona, el elemento activo del menú, algún acento).

## Logo → símbolo
`partials/mark.html` es un SVG inline de 24×24 en `currentColor`, que se usa en la barra lateral, el login y los estados vacíos. Redibuja el elemento más reconocible del logo (en nuestra demo de referencia, el tejado: tres trazos). No metas el logo completo en raster ahí. El logo completo puede ir en `static/img/` y usarse en el login si queda mejor. El favicon (`static/img/favicon.svg`) es el símbolo sobre un cuadrado con el color de marca o el neutro oscuro.

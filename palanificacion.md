# Planificacion del proyecto

## Alcance

Este documento analiza la copia de desarrollo ubicada en:

`/home/erichy/Work/anki-markdown-katex-improved`

El add-on original instalado en Anki queda fuera del alcance y no debe modificarse directamente:

`/home/erichy/.local/share/Anki2/addons21/1087328706`

## Resumen general

El proyecto es un add-on de Anki que agrega soporte para Markdown, KaTeX, bloques de codigo con resaltado, formulas quimicas y tarjetas Cloze/Basic especiales.

La idea base es buena y util, pero la implementacion actual es fragil. Muchos errores reportados por usuarios siguen presentes en esta copia, especialmente los relacionados con el simbolo `$`, modo oscuro, estilos Cloze, vista previa y limpieza de HTML pegado.

## Estructura del proyecto

Archivos propios principales:

- `__init__.py`: logica Python del add-on. Crea modelos, registra hooks y copia recursos al media folder de Anki.
- `HTMLandCSS.py`: contiene HTML, CSS y JavaScript embebido para las tarjetas y la vista previa.
- `meta.json`: metadata del add-on.

Recursos externos incluidos localmente:

- `_katex.min.js`
- `_katex.css`
- `_auto-render.js`
- `_markdown-it.min.js`
- `_markdown-it-mark.js`
- `_highlight.js`
- `_highlight.css`
- `_mhchem.js`
- `fonts/`

## Funcionalidades implementadas

### Creacion automatica de tipos de nota

El add-on crea automaticamente dos tipos de nota:

- `KaTeX and Markdown Basic`
- `KaTeX and Markdown Cloze`

Referencias:

- `__init__.py:44-58`
- `__init__.py:60-100`

### Tipo Basic

Campos:

- `Front`
- `Back`

Plantillas:

- `front`
- `back`

Referencia:

- `__init__.py:60-79`

### Tipo Cloze

Campos:

- `Text`
- `Back Extra`

Plantillas:

- `front_cloze`
- `back_cloze`

Referencia:

- `__init__.py:81-100`

### Soporte Markdown

Usa `markdown-it 12.0.4`.

Permite:

- Titulos.
- Listas.
- Tablas.
- Links.
- Bloques de codigo.
- HTML embebido.
- Marcado `==texto==` mediante `_markdown-it-mark.js`.

Referencias:

- `HTMLandCSS.py:117`
- `HTMLandCSS.py:227`
- `HTMLandCSS.py:344`
- `HTMLandCSS.py:450`
- `HTMLandCSS.py:564`

### Soporte KaTeX

Usa KaTeX para renderizar formulas matematicas.

Delimitadores activos actualmente:

```js
{left: "$$", right: "$$", display: true}
{left: "$", right: "$", display: false}
```

Referencias:

- `HTMLandCSS.py:109-112`
- `HTMLandCSS.py:218-221`
- `HTMLandCSS.py:336-339`
- `HTMLandCSS.py:442-445`
- `HTMLandCSS.py:556-559`

### Soporte de quimica

Usa `_mhchem.js` para soportar expresiones como:

```tex
\ce{H2O}
\pu{10 g}
```

Referencias:

- `HTMLandCSS.py:55`
- `HTMLandCSS.py:163`
- `HTMLandCSS.py:278`
- `HTMLandCSS.py:391`
- `HTMLandCSS.py:498`

### Resaltado de codigo

Usa Highlight.js `11.0.1`.

Ejemplo de uso:

````markdown
```python
print("hola")
```
````

Referencias:

- `HTMLandCSS.py:117-125`
- `HTMLandCSS.py:227-235`
- `HTMLandCSS.py:344-352`
- `HTMLandCSS.py:450-458`
- `HTMLandCSS.py:564-572`

### Vista previa en el editor

La funcion `markdownPreview(editor)` inyecta una preview Markdown/KaTeX en el editor de Anki cuando la nota usa uno de los modelos del add-on.

Referencias:

- `__init__.py:13-41`
- `HTMLandCSS.py:3-147`

### Copia de recursos al media folder

La funcion `update()` copia JS, CSS y fuentes al directorio media de Anki.

Referencias:

- `__init__.py:103-145`

### Fallback a CDN

Si falla la carga local de recursos, el add-on intenta cargar desde CDNs externos como `cdn.jsdelivr.net` y `cdnjs.cloudflare.com`.

Esto mejora la probabilidad de carga, pero afecta privacidad, reproducibilidad y soporte offline real.

## Flujo de ejecucion

1. Anki carga el perfil.
2. Se ejecuta `create_model_if_necessacy()` mediante hook.
3. El add-on busca los modelos Basic y Cloze.
4. Si no existen, los crea.
5. Ejecuta `update()`.
6. `update()` copia recursos al media folder de la coleccion.
7. Al abrir una nota, `markdownPreview(editor)` inyecta JS en el editor.
8. Al revisar una tarjeta, la plantilla carga recursos JS/CSS.
9. Primero ejecuta KaTeX.
10. Despues ejecuta Markdown.
11. Finalmente muestra el contenido cambiando `visibility` a `visible`.

## Errores encontrados

### 1. Bug grave con `$`

Estado: no corregido.

El add-on activa `$...$` como formula inline. Esto rompe textos normales con dinero, variables de shell, PHP, jQuery y otros usos comunes.

Ejemplos problematicos:

```text
Alice sent $500 to Bob. Now Bob has $1000.
echo $HOME and $PATH
Price: $100, $50 more than Bob.
```

Resultado esperado:

- El texto debe mantenerse literal.

Resultado actual:

- Partes del texto son interpretadas como formulas KaTeX.

Referencias:

- `HTMLandCSS.py:110-111`
- `HTMLandCSS.py:219-220`
- `HTMLandCSS.py:337-338`
- `HTMLandCSS.py:443-444`
- `HTMLandCSS.py:557-558`

Nota importante: `_auto-render.js` trae `$...$` comentado por defecto porque rompe texto normal, pero las plantillas lo vuelven a activar manualmente.

### 2. `$` dentro de bloques de codigo se rompe

Estado: no corregido.

El add-on procesa KaTeX antes que Markdown. Por eso, cuando KaTeX corre, un bloque Markdown todavia no es un elemento `<code>` o `<pre>` real.

Ejemplo problematico:

````markdown
```bash
echo $HOME
```
````

Resultado actual:

- `$HOME` puede ser tratado como inicio de formula.

Referencias:

- `HTMLandCSS.py:94-97`
- `HTMLandCSS.py:203-206`
- `HTMLandCSS.py:317-322`
- `HTMLandCSS.py:429-432`
- `HTMLandCSS.py:538-543`

### 3. Escape `\$` no confiable

Estado: no corregido.

Usuarios reportaron que escapar el dolar con `\$` no funciona correctamente o deja barras visibles. La logica actual de delimitadores no resuelve bien todos los casos.

### 4. Modo oscuro incompleto

Estado: no corregido.

El CSS base no define reglas para `.nightMode`.

CSS actual relevante:

- `HTMLandCSS.py:597-619`

Faltan reglas para:

- `.nightMode .card`
- `.nightMode code`
- `.nightMode pre code`
- `.nightMode table`
- `.nightMode .hljs`
- `.nightMode .cloze`
- `blockquote`
- `mark`

Esto confirma los comentarios donde el texto queda blanco sobre fondo blanco, especialmente en bloques de codigo.

### 5. Cloze styling roto

Estado: no corregido.

El codigo elimina todos los `span`:

```js
str = str.replace(/<[\/]?span[^>]*>/gi, "")
```

Referencias:

- `HTMLandCSS.py:135`
- `HTMLandCSS.py:245`
- `HTMLandCSS.py:362`
- `HTMLandCSS.py:468`
- `HTMLandCSS.py:582`

Anki usa `span.cloze` para tarjetas Cloze. Al eliminar estos `span`, se pierde la clase `.cloze` y no funcionan estilos personalizados.

### 6. Limpieza de copy/paste fragil

Estado: parcialmente corregido, pero con efectos secundarios.

El add-on intenta limpiar HTML pegado desde otros editores eliminando etiquetas como `span`, `pre`, `div` y `br` con regex.

Referencias:

- `HTMLandCSS.py:130-137`
- `HTMLandCSS.py:240-247`
- `HTMLandCSS.py:357-364`
- `HTMLandCSS.py:463-470`
- `HTMLandCSS.py:577-584`

Problemas:

- Rompe Cloze.
- Puede destruir HTML valido.
- No distingue entre etiquetas basura y etiquetas necesarias.

### 7. Bug de `replace` sin asignacion

Estado: no corregido.

Hay llamadas como:

```js
str.replace(/<\/div[^>]*>/g, "\\n");
```

Pero el resultado no se reasigna a `str`, asi que no tiene efecto.

Referencias:

- `HTMLandCSS.py:136`
- `HTMLandCSS.py:246`
- `HTMLandCSS.py:363`
- `HTMLandCSS.py:469`
- `HTMLandCSS.py:583`

### 8. Riesgo de seguridad por `html:true`

Estado: no corregido.

Markdown-it esta configurado con `html:true`.

Referencias:

- `HTMLandCSS.py:117`
- `HTMLandCSS.py:227`
- `HTMLandCSS.py:344`
- `HTMLandCSS.py:450`
- `HTMLandCSS.py:564`

Esto permite HTML arbitrario dentro de las notas. Puede ser util para usuarios avanzados, pero es riesgoso si se importan tarjetas de fuentes externas.

### 9. Preview fragil en Anki moderno

Estado: no corregido.

La preview depende de estructura interna del editor:

```js
fields.children[0].children[1].shadowRoot.children[2].innerHTML
```

Referencias:

- `HTMLandCSS.py:18-19`
- `HTMLandCSS.py:30-31`

Esto puede romperse con cambios de Anki, Qt o el editor.

### 10. Preview limitada a dos campos

Estado: no corregido.

La preview siempre lee solo campo 1 y campo 2.

Referencias:

- `HTMLandCSS.py:18-20`
- `HTMLandCSS.py:30-32`

No soporta modelos con mas campos ni campos personalizados.

### 11. Posible acumulacion de listeners

Estado: no corregido.

Cada carga agrega un listener:

```js
document.addEventListener('keyup', keyupFunc);
```

Referencia:

- `HTMLandCSS.py:52`

No se remueve el listener anterior. Puede causar renders duplicados o lentitud.

### 12. Variables globales implicitas

Estado: no corregido.

Variables como `keyupFunc` y `main` se asignan sin `let`, `const` o `var`.

Referencias:

- `HTMLandCSS.py:17`
- `HTMLandCSS.py:29`
- `HTMLandCSS.py:50`

Esto contamina el scope global del WebView.

### 13. Codigo altamente duplicado

Estado: no corregido.

Funciones repetidas en varias plantillas:

- `getScript`
- `getCSS`
- `renderMath`
- `markdown`
- `replaceInString`
- `replaceHTMLElementsInString`

Consecuencias:

- Dificulta mantenimiento.
- Aumenta riesgo de inconsistencias.
- Obliga a corregir el mismo bug en multiples lugares.

### 14. Error en fallback CSS

Estado: no corregido.

En una plantilla aparece:

```js
css.onerror = reject;
```

Deberia asignarse al objeto del CSS online.

Referencia:

- `HTMLandCSS.py:193`

### 15. Dependencias antiguas

Estado: no corregido.

Versiones detectadas:

- `markdown-it 12.0.4`
- `highlight.js 11.0.1`
- KaTeX enlazado a CDN `0.12.0`
- mhchem enlazado a CDN `0.13.11`

Esto puede afectar compatibilidad, seguridad y soporte de nuevas funciones.

### 16. Fallback remoto contradice soporte offline real

Estado: parcialmente corregido.

Hay recursos locales, pero si fallan se intenta cargar desde CDN.

Referencias:

- `HTMLandCSS.py:39-47`
- `HTMLandCSS.py:154-161`
- `HTMLandCSS.py:269-276`
- `HTMLandCSS.py:382-389`
- `HTMLandCSS.py:489-496`

Problemas:

- Menor privacidad.
- Dependencia de internet.
- Posible lentitud.
- Fallos por red o politicas de seguridad.

### 17. Actualizacion incompleta de recursos

Estado: no corregido.

`_add_file()` solo copia si el archivo no existe:

```python
if not os.path.isfile(os.path.join(mw.col.media.dir(), filename)):
    mw.col.media.add_file(path)
```

Referencias:

- `__init__.py:143-145`

Si ya existe una version vieja del recurso en media, no se reemplaza.

### 18. Borrado potencialmente peligroso

Estado: no corregido.

`update()` borra carpetas del media folder:

```python
shutil.rmtree(...)
```

Referencias:

- `__init__.py:120-124`

Si otro add-on o el usuario usa esas carpetas, podria eliminar contenido no relacionado.

### 19. API antigua de Anki

Estado: no corregido.

Usa:

```python
from anki.hooks import addHook
```

Referencias:

- `__init__.py:6`
- `__init__.py:41`
- `__init__.py:148`

En Anki moderno conviene migrar a `aqt.gui_hooks`.

### 20. Metadata vieja

Estado: no corregido.

`meta.json` declara:

```json
"max_point_version": 42
```

Referencia:

- `meta.json:1`

Esto indica compatibilidad maxima antigua, aproximadamente Anki 2.1.42.

### 21. Typo en nombre de funcion

Estado: no corregido.

La funcion se llama:

```python
create_model_if_necessacy
```

Referencia:

- `__init__.py:44`

No rompe el add-on, pero deberia ser `necessary`.

### 22. `CONF_NAME` no se usa

Estado: no corregido.

`CONF_NAME` esta definido pero no tiene uso real.

Referencia:

- `__init__.py:10`

### 23. No hay tests

Estado: no corregido.

No existe suite de pruebas para:

- Parseo de `$`.
- Render Markdown.
- Cloze.
- Dark mode.
- Copy/paste.
- Preview.
- Instalacion en Anki moderno.

### 24. No hay documentacion del proyecto

Estado: corregido parcialmente por este documento.

Antes de este archivo no habia `README.md`, guia de desarrollo ni instrucciones de prueba.

## Comparacion con comentarios de usuarios

| Problema reportado | Estado en esta copia | Evidencia |
|---|---|---|
| `$` con dinero se interpreta como KaTeX | No corregido | Plantillas activan `$...$` |
| `$HOME`, Bash, PHP, jQuery se rompen | No corregido | KaTeX corre antes que Markdown |
| Escape `\$` falla o se ve feo | No corregido | Logica de delimitadores insuficiente |
| Modo oscuro ilegible | No corregido | No hay `.nightMode` |
| Bloques de codigo blancos en dark mode | No corregido | `_highlight.css` usa tema claro |
| Inline code sin estilo especial | No corregido | CSS solo define `pre code`, no `code` |
| Cloze no permite CSS personalizado | No corregido | Se eliminan todos los `span` |
| Copy/paste mete `span` o CSS | Parcialmente corregido, defectuoso | Limpieza con regex rompe Cloze |
| Preview no funciona en Linux/moderno | Probablemente no corregido | Usa `shadowRoot.children[...]` |
| CSS no se guarda | Parcialmente corregido | Update de templates esta comentado |
| Syntax highlighting falla en algunos lenguajes | Parcialmente no corregido | Highlight.js viejo/default |
| Quimica falla a veces | No confirmado | mhchem existe, pero depende del orden de carga |
| AnkiWeb funciona | Probablemente si | Plantillas usan HTML/JS y recursos en media/CDN |
| Offline support | Parcial | Recursos locales + fallback remoto |
| Falta de instrucciones | Parcialmente corregido | Este documento inicia la documentacion |
| Compatibilidad con Anki moderno | Riesgosa | `addHook`, `editor.web.eval`, `max_point_version: 42` |

## Diagnostico de calidad

El add-on es funcional, pero esta muy acoplado:

- Python crea modelos y copia recursos.
- HTML, CSS y JavaScript estan embebidos en strings gigantes.
- El mismo JavaScript se repite en varias plantillas.
- El orden de renderizado causa bugs.
- La limpieza de HTML con regex destruye informacion valida.
- No hay pruebas automatizadas.
- No hay separacion clara entre librerias externas y codigo propio.

La mayor deuda tecnica esta en `HTMLandCSS.py`.

## Prioridades para una nueva version

### Prioridad 1: corregir `$`

Opciones:

- Desactivar `$...$` por defecto.
- Usar solo `$$...$$`, `\(...\)` y `\[...\]` por defecto.
- Hacer `$...$` configurable.
- Permitir `$...$` solo si no esta pegado a letras o numeros.
- Ignorar `$` dentro de codigo inline y bloques de codigo.

Recomendacion:

- Por defecto usar `$$...$$`, `\(...\)` y `\[...\]`.
- Agregar opcion para activar `$...$` en modo compatibilidad Obsidian.

### Prioridad 2: cambiar orden de renderizado

Renderizar primero Markdown y despues KaTeX sobre el DOM resultante, respetando `ignoredTags: ["pre", "code"]`.

Esto evita que `$HOME` dentro de codigo se procese como formula.

### Prioridad 3: preservar Cloze

No eliminar `span.cloze`.

La limpieza debe distinguir entre:

- `span` basura de copy/paste.
- `span.cloze` generado por Anki.
- `span` generado por KaTeX.

### Prioridad 4: agregar dark mode real

CSS minimo necesario:

- `.nightMode .card`
- `.nightMode code`
- `.nightMode pre code`
- `.nightMode table`
- `.nightMode .hljs`
- `.nightMode .cloze`
- `mark`
- `blockquote`

### Prioridad 5: separar codigo repetido

Extraer logica comun de renderizado.

Objetivo:

- Una unica funcion de carga de recursos.
- Una unica funcion de render Markdown.
- Una unica funcion de render KaTeX.
- Una unica funcion de limpieza.
- Plantillas Basic/Cloze mas pequenas.

### Prioridad 6: modernizar compatibilidad con Anki

Migrar:

- `anki.hooks.addHook` a `aqt.gui_hooks`.
- `editor.web.eval` a una integracion mas estable si es posible.
- Acceso fragil a campos del editor por una API o selector mas robusto.

### Prioridad 7: recursos locales por defecto

Eliminar fallback remoto o hacerlo configurable.

Recomendacion:

- Modo default: solo recursos locales.
- Modo opcional: fallback remoto, desactivado por defecto.

### Prioridad 8: actualizar dependencias

Actualizar con pruebas:

- KaTeX.
- markdown-it.
- highlight.js.
- mhchem compatible con la version de KaTeX elegida.

### Prioridad 9: agregar pruebas

Casos minimos:

```text
$500 no debe ser formula
$HOME no debe ser formula
$x+1$ solo debe ser formula si el modo $ esta activo
Bloques bash con $HOME no deben renderizar KaTeX
{{c1::texto}} debe conservar .cloze
==texto== debe renderizar mark
Dark mode debe mantener contraste legible
```

### Prioridad 10: documentacion

Crear:

- `README.md`
- Guia de instalacion de desarrollo.
- Guia de pruebas manuales.
- Changelog.
- Lista de decisiones de compatibilidad.

## Plan recomendado de implementacion

### Fase 1: preparacion

1. Crear `README.md`.
2. Crear `ROADMAP.md` o mantener este archivo como documento vivo.
3. Cambiar nombre del modelo de desarrollo para no pisar el original, por ejemplo `KaTeX and Markdown Improved`.
4. Definir estrategia de instalacion como add-on separado.

### Fase 2: bugs criticos

1. Corregir `$`.
2. Cambiar orden a Markdown primero, KaTeX despues.
3. Evitar render KaTeX dentro de `pre` y `code`.
4. Agregar CSS dark mode.
5. Preservar `span.cloze`.

### Fase 3: mantenimiento

1. Reducir duplicacion en `HTMLandCSS.py`.
2. Extraer JS comun.
3. Corregir `replace` sin asignacion.
4. Eliminar variables globales implicitas.
5. Evitar listeners duplicados.

### Fase 4: compatibilidad moderna

1. Migrar hooks a `aqt.gui_hooks`.
2. Revisar integracion con editor moderno.
3. Hacer preview dinamica para mas de dos campos.
4. Actualizar `meta.json`.

### Fase 5: dependencias y seguridad

1. Actualizar librerias.
2. Decidir si `html:true` queda activo, configurable o desactivado.
3. Eliminar fallback CDN por defecto.
4. Versionar recursos copiados al media folder.

## Propuesta de nueva version

Nombre sugerido:

`Markdown and KaTeX Improved`

Objetivos principales:

- No romper texto normal con `$`.
- Funcionar bien en modo oscuro.
- Respetar estilos Cloze.
- Soportar codigo de programacion sin falsos positivos.
- Mantener soporte offline real.
- Ser compatible con Anki moderno.
- Tener estructura mantenible.

## Conclusion

La copia actual conserva la mayoria de los errores reportados por usuarios. La funcionalidad base es valiosa, pero para una version mejorada conviene atacar primero `$`, Cloze, dark mode y orden de renderizado.

Despues de esos arreglos, el siguiente paso natural es refactorizar `HTMLandCSS.py` para reducir duplicacion y modernizar la integracion con Anki.

# Planificacion del proyecto

## Alcance

Este documento analiza la copia de desarrollo ubicada en:

`/home/erichy/Work/anki-markdown-katex-improved`

El add-on original instalado en Anki queda fuera del alcance y no debe modificarse directamente:

`/home/erichy/.local/share/Anki2/addons21/1087328706`

## Resumen general

El proyecto es un add-on de Anki que agrega soporte para Markdown, KaTeX, bloques de codigo con resaltado, formulas quimicas y tarjetas Cloze/Basic especiales.

La idea base es buena y util, pero la implementacion actual es fragil. Muchos errores reportados por usuarios siguen presentes en esta copia, especialmente los relacionados con el simbolo `$`, modo oscuro, estilos Cloze, vista previa y limpieza de HTML pegado.

## Estado actualizado

Actualizado despues de las correcciones realizadas en la rama de desarrollo `main`.

El analisis historico de este documento conserva referencias y estados originales para entender la deuda tecnica inicial. La fuente de verdad para el estado actual es esta seccion y el roadmap actualizado al final.

### Ya corregido

- Se creo una instalacion de desarrollo separada mediante symlink `markdownkatexdev`, sin modificar el add-on original instalado.
- Se desactivo `$...$` como delimitador KaTeX por defecto.
- Se mantienen como delimitadores validos `$$...$$`, `\(...\)` y `\[...\]`.
- El render ahora ejecuta Markdown antes que KaTeX.
- KaTeX ignora `script`, `noscript`, `style`, `textarea`, `pre` y `code`.
- Se preserva `span.cloze` para no romper estilos Cloze.
- Se agrego modo oscuro real con tema Catppuccin Latte/Mocha.
- Se aplico estilo Catppuccin a tarjetas, preview del editor y Highlight.js.
- Se corrigio el bug de `replace` sin asignacion.
- Se extrajeron helpers JS comunes para reducir duplicacion en las plantillas.
- Se mitigaron listeners duplicados en la preview del editor.
- Se migraron hooks legacy `addHook` a `aqt.gui_hooks`.
- Se corrigieron APIs deprecadas de Anki moderno: `byName` -> `by_name` y `note.model()` -> `note.note_type()`.
- Se actualizo `meta.json` para Anki moderno.
- Se corrigieron errores CSP de Anki 26.05 en la preview cargando recursos desde `/_addons/...`.
- Se corrigieron rutas de fuentes KaTeX en la preview para cargarlas desde `/_addons/<addon>/fonts/...`.
- La preview del editor soporta mas de dos campos y muestra nombres reales de campos (`Front`, `Back`, `Text`, `Back Extra`).
- Se agrego `TESTING.md` con checklist manual.

### Pendiente

- Actualizar este documento por completo si se desea eliminar referencias historicas obsoletas.
- Mantener `html:true` activo para preservar compatibilidad; cambiarlo seria una decision de ruptura separada.
- Verificar manualmente que las tarjetas finales cargan correctamente solo con recursos locales.
- Actualizar dependencias externas con pruebas, de a una por vez: KaTeX, markdown-it, Highlight.js y mhchem.
- Definir si hace falta versionar recursos copiados al media folder.
- Mantener `editor.web.eval` por ahora; funciona en Anki 26.05 y no hay bug concreto que justifique cambiarlo.
- Continuar separando la preview del editor si futuros cambios lo justifican.
- Mejorar la limpieza de HTML pegado; sigue basada en regex y puede tener efectos secundarios.
- Definir si hace falta versionar recursos copiados al media folder.
- Ampliar tests automatizados cuando se actualicen dependencias o aparezcan nuevos casos borde.

### Decisiones de Fase 1

- `README.md` queda como documentacion principal para instalacion, uso y desarrollo.
- `ROADMAP.md` queda como roadmap corto y actual; este archivo conserva el analisis historico extendido.
- Los tipos de nota mantienen los nombres actuales por ahora: `KaTeX and Markdown Basic` y `KaTeX and Markdown Cloze`.
- No se renombran a `KaTeX and Markdown Improved` todavia porque eso puede requerir una migracion de notas/modelos existentes.

## Estructura del proyecto

Archivos propios principales:

- `__init__.py`: logica Python del add-on. Crea modelos, registra hooks y copia recursos al media folder de Anki.
- `HTMLandCSS.py`: contiene la preview del editor, helpers JS compartidos y generacion de plantillas finales.
- `_card.css`: contiene el CSS de tarjetas que se inyecta en los modelos de Anki.
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

Estado actual: eliminado de las tarjetas finales. Si falla la carga local de recursos, la tarjeta se muestra sin intentar cargar CDNs externos.

Esto mejora privacidad, reproducibilidad y soporte offline real. La verificacion manual debe confirmar que todos los recursos locales se copian correctamente al media folder.

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

### 8. Politica de `html:true`

Estado: decidido mantener activo.

Markdown-it esta configurado con `html:true`.

Referencias:

- `HTMLandCSS.py:117`
- `HTMLandCSS.py:227`
- `HTMLandCSS.py:344`
- `HTMLandCSS.py:450`
- `HTMLandCSS.py:564`

Esto permite HTML arbitrario dentro de las notas. Se mantiene para preservar compatibilidad con tarjetas existentes y usuarios avanzados. Desactivarlo o hacerlo configurable queda fuera de este ciclo porque podria romper contenido existente.

### 9. Preview fragil en Anki moderno

Estado: evaluado; mantener implementacion actual por ahora.

La preview depende de estructura interna del editor:

```js
fields.children[0].children[1].shadowRoot.children[2].innerHTML
```

Referencias:

- `HTMLandCSS.py:18-19`
- `HTMLandCSS.py:30-31`

Esto puede romperse con cambios de Anki, Qt o el editor. Por ahora funciona en Anki 26.05 y no se cambia sin un bug concreto.

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
- KaTeX local basado en version `0.12.0`
- mhchem local basado en version `0.13.11`

Se intento actualizar en bloque a versiones nuevas, pero rompio el renderizado y se revirtio. La actualizacion debe hacerse de a una dependencia por vez con validacion manual en Anki.

### 16. Fallback remoto contradice soporte offline real

Estado: corregido en tarjetas finales; pendiente verificar recursos locales copiados al media folder.

Las tarjetas finales cargan recursos locales y ya no intentan cargar desde CDN si falla un recurso.

Referencias:

- `HTMLandCSS.py:39-47`
- `HTMLandCSS.py:154-161`
- `HTMLandCSS.py:269-276`
- `HTMLandCSS.py:382-389`
- `HTMLandCSS.py:489-496`

Problemas:

- Si falta un recurso local, la tarjeta se muestra sin render avanzado.
- Queda verificar manualmente que los recursos reemplazados se cargan correctamente desde el media folder.

### 17. Actualizacion incompleta de recursos

Estado: corregido.

`_add_file()` ahora compara el recurso empaquetado con la copia del media folder y reemplaza la copia si el contenido cambio:

```python
if os.path.isfile(target) and filecmp.cmp(path, target, shallow=False):
    return
```

Referencias:

- `__init__.py:143-145`

Si ya existe una version vieja del recurso en media, se reemplaza manteniendo el mismo nombre que usan las plantillas.

### 18. Borrado potencialmente peligroso

Estado: corregido.

`update()` ya no borra carpetas completas del media folder. Antes existia este patron:

```python
shutil.rmtree(...)
```

Referencias:

- `__init__.py:120-124`

Se elimino para evitar borrar contenido no relacionado si otro add-on o el usuario usa nombres similares.

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

Estado: corregido parcialmente.

Existe `tests/test_render_contract.py` con checks automatizados para comportamiento sensible. Todavia no reemplaza las pruebas manuales completas de Anki.

Cobertura inicial:

- `$...$` desactivado como delimitador.
- KaTeX ignorando `pre` y `code`.
- Cloze preservado.
- `markdown-it-mark` activo.
- CSS de dark mode presente.
- Preview con recursos `/_addons/...` y sin CDN.
- Plantillas Basic/Cloze conservando campos esperados.
- `update()` sin `shutil.rmtree`.

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
| AnkiWeb funciona | Pendiente de verificar | Plantillas usan HTML/JS y recursos locales en media |
| Offline support | Mejorado, pendiente de prueba manual | Recursos locales sin fallback remoto |
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

## Prioridades actuales

### Prioridad 1: documentacion y cierre de fase

- Estado: completada para Fase 1.
- `README.md` documenta instalacion, uso, tipos de nota, delimitadores soportados y advertencias.
- `ROADMAP.md` documenta fases, pendientes y recomendaciones.
- `TESTING.md` documenta pruebas manuales.
- La instalacion de desarrollo con symlink `markdownkatexdev` queda documentada.
- Las decisiones de compatibilidad quedan documentadas: `$...$` desactivado, recursos locales para preview, soporte Anki 2.1.20+.

### Prioridad 2: recursos locales y media folder

- Fallback CDN eliminado en tarjetas finales; verificar manualmente el comportamiento offline.
- `_add_file()` actualiza recursos ya existentes en el media folder cuando cambia el contenido.
- Borrados amplios con `shutil.rmtree()` eliminados de `update()`.
- Definir estrategia de versionado de assets copiados a media.

### Prioridad 3: seguridad y configuracion

- `html:true` queda activo para preservar compatibilidad.
- Reconsiderar solo si se planifica un cambio de ruptura o una configuracion explicita.
- Definir si se agrega configuracion para reactivar `$...$` en modo compatibilidad.

### Prioridad 4: refactor de `HTMLandCSS.py`

- Plantillas finales generadas desde un constructor comun: completado.
- CSS de tarjetas separado en `_card.css`: completado.
- Reducir strings gigantes embebidos en Python: completado parcialmente.
- Mantener compatibilidad con Basic, Cloze y preview del editor.
- Continuar separando preview del editor solo si futuros cambios lo requieren.

### Prioridad 5: integracion moderna con Anki

- `editor.web.eval` fue evaluado y se mantiene mientras no haya un bug concreto.
- Mantener recursos del editor servidos desde `/_addons/...` para cumplir CSP.
- Seguir probando en Anki 26.05 y versiones modernas.

### Prioridad 6: dependencias

- Actualizar KaTeX de a una version controlada con pruebas de formulas y fuentes.
- Actualizar markdown-it de forma separada con pruebas de Markdown, tablas y HTML.
- Actualizar Highlight.js de forma separada con pruebas de Bash, Java, C, C++, Python y otros lenguajes usados.
- Confirmar version compatible de mhchem con la version de KaTeX elegida.

### Prioridad 7: pruebas automatizadas

Estado: cobertura inicial completada.

Casos minimos:

```text
$500 no debe ser formula
$HOME no debe ser formula
$x+1$ solo debe ser formula si el modo $ esta activo
Bloques bash con $HOME no deben renderizar KaTeX
{{c1::texto}} debe conservar .cloze
==texto== debe renderizar mark
Dark mode debe mantener contraste legible
Preview no debe disparar errores CSP
Recursos KaTeX deben cargar fuentes desde la ruta correcta
```

## Plan recomendado de implementacion actualizado

### Fase 1: base de desarrollo

Estado: completada.

- Instalacion de desarrollo separada: completado.
- Add-on original fuera de alcance: completado.
- `TESTING.md`: completado.
- `README.md`: completado.
- `ROADMAP.md`: completado.
- Renombrar modelos a `KaTeX and Markdown Improved`: decidido no hacerlo por ahora; queda como posible migracion futura.

### Fase 2: bugs criticos de render

Estado: completada.

- Corregir `$`: completado.
- Cambiar orden a Markdown primero y KaTeX despues: completado.
- Evitar render KaTeX dentro de `pre` y `code`: completado.
- Agregar CSS dark mode: completado.
- Preservar `span.cloze`: completado.

### Fase 3: mantenimiento inicial

Estado: completada parcialmente.

- Reducir duplicacion en `HTMLandCSS.py`: completado.
- Extraer JS comun: completado parcialmente.
- Corregir `replace` sin asignacion: completado.
- Eliminar variables globales implicitas principales: completado.
- Evitar listeners duplicados: completado.
- Refactor profundo de `HTMLandCSS.py`: completado para plantillas finales y CSS de tarjetas.

### Fase 4: compatibilidad moderna

Estado: completada parcialmente.

- Migrar hooks a `aqt.gui_hooks`: completado.
- Actualizar `meta.json`: completado.
- Corregir APIs deprecadas `byName` y `note.model()`: completado.
- Corregir CSP de preview en Anki 26.05: completado.
- Corregir rutas de fuentes KaTeX en preview: completado.
- Preview dinamica para mas de dos campos: completado.
- Evaluar reemplazo de `editor.web.eval`: completado; se mantiene por ahora.

### Fase 5: dependencias y seguridad

Estado: completada parcialmente.

- Actualizar librerias: pendiente; la actualizacion en bloque fue revertida porque rompio el render.
- Decidir politica de `html:true`: completado; se mantiene activo para compatibilidad.
- Eliminar o hacer configurable fallback CDN en tarjetas finales: completado; las tarjetas finales cargan recursos locales.
- Reemplazar recursos obsoletos en media folder: completado.
- Evitar borrados amplios con `shutil.rmtree()`: completado.
- Versionar recursos copiados al media folder: pendiente de decision.

Recomendacion: seguir con actualizacion de dependencias usando los tests automatizados y el checklist manual.

### Fase 6: documentacion y publicacion

Estado: pendiente.

- Crear `README.md`: completado.
- Crear changelog: completado en `CHANGELOG.md`.
- Agregar tests automatizados de render: completado con cobertura inicial.
- Documentar pruebas manuales finales: parcialmente completado en `TESTING.md`.
- Preparar commit/release cuando el usuario lo solicite: pendiente.

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

## Conclusion actualizada

La copia de desarrollo ya resolvio los problemas criticos iniciales de `$`, orden de renderizado, Cloze, modo oscuro y compatibilidad basica con Anki 26.05.

El siguiente paso natural es avanzar con actualizacion de dependencias usando los tests automatizados y el checklist manual, y luego crear un changelog inicial.

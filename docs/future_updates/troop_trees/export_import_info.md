# Export/Import de Árboles de Tropas — Resumen Técnico

Documento de conclusión: explica **cómo funciona** la persistencia de los árboles
de tropas personalizados del reino (guardar / cargar / borrar), **dónde** se guardan
los datos, **por qué** se eligió JSON plano y **cómo llega al jugador**. Es la
referencia final para quien venga después.

---

## 1. Panorama

El flujo completo vive en el mod `kingdom_custom_troop_tree_creator`:

1. **Picker** (`prsnt_cstm_choose_troop_tree`) — elige rama + género + "Elegir".
2. **Creador** (`prsnt_cstm_create_troop_tree`) — muestra el árbol, edita el
   prefijo, edita cada tropa (store), botón **Export**.
3. **Pantalla de gestión** (`prsnt_kct_manage_tree_files`) — desde el botón
   **Import** del picker: lista 8 slots, carga o borra árboles guardados.

Toda la persistencia usa dos mecanismos de **WSE2** (obligatorio para el mod a
partir de ahora):

- `dict_*` (3200-3218) → archivos **JSON** legibles (datos del árbol).
- `array_*` (5003/5004) → archivos **binarios `.wsearray`** (registro slot→nombre).

No existe opcode de escritura de texto plano (`str_save_to_file` no existe en WSE),
así que las dos únicas vías de guardado son las de arriba.

---

## 2. Dónde se guardan los archivos

En el **directorio gestionado por WSE2** del módulo, **fuera** de la carpeta del
módulo y **fuera** de la carpeta de partidas:

```
Documents\Mount&Blade Warband WSE2\WSE\<nombre_del_módulo>\
    ├── kct trees.wsearray      # registro de 8 slots (binario)
    └── <prefijo>.json          # un archivo por árbol guardado (legible)
```

- La ruta real puede fijarse con `storage_path` en `wse_settings.ini`.
- Los archivos **se crean automáticamente** la primera vez que el juego los usa;
  no se distribuyen con el módulo.

---

## 3. El registro de slots (`kct trees.wsearray`)

- Cadena `@kct_trees` = `kct_tree_registry_file` (`kingdom_custom_troop_tree_creator_constants.py:85`).
- Array unidimensional de `kct_tree_slot_count = 8` entradas de string.
- Entrada `i` = nombre del árbol en el slot `i`; string vacío = slot libre.
- Binario (`array_save_file` / `array_load_file`); el jugador **no** lo edita a mano.
- Autocuración: si el archivo no existe o tiene un tamaño distinto de 8, el código
  lo recrea/vuelve a generar y lo reescribe (`tree_files.py:88-119`,
  `tree_io.py:187-199`).

---

## 4. Los datos del árbol (`<prefijo>.json`)

Escrito por `script_kct_export_tree_to_file` (`tree_io.py:90-170`) con
`dict_save_json`; leído por `script_kct_import_tree_from_file` con
`dict_load_file_json`.

### Esquema (JSON plano, claves generadas)

```
kct_version   = 1            (int, para migraciones futuras)
kct_tree      = 0..3         (int, índice del preset de rama)
kct_count     = N            (int, número de tropas)
kct_prefix    = "Calradian"  (string, prefijo / nombre del árbol)

Por cada tropa i:
  t{i}_name        (string, nombre singular — del dummy)
  t{i}_plural      (string, nombre plural — del dummy)
  t{i}_att{j}      j=0..3          (atributos)
  t{i}_skl{j}      j=0..41         (42 habilidades)
  t{i}_wpt{j}      j=0..6          (7 proficiencias)
  t{i}_eq_item{j}  /  t{i}_eq_mod{j}   j=0..num_equipment_kinds-1  (equipo + modificadores)
  t{i}_conf        (int, flag de configurado)
```

### ¿Por qué plano?

WSE **no tiene arrays ni dicts anidados**: `dict_save_json` serializa un mapa plano
clave→escalar (int/float/string/posición). No hay `dict_set_dict`. Por eso la
"jerarquía" se codifica en el **nombre de la clave** (`t{i}_skl{j}`) en lugar de
en estructuras anidadas. El export y el import generan las mismas claves en
`try_for_range`, así el índice vive en el string.

Esto también depende de que la forma del árbol es fija: cada preset tiene un nº
de tropas conocido (7/6/5/22) y campos de ancho fijo, por lo que el espacio de
claves es determinista y el import puede validar `kct_count` contra el rango
actual (`tree_io.py:264-270`).

### ¿Por qué JSON y no txt?

No fue una elección libre: WSE solo ofrece tres formatos de guardado:

| Opcode | Formato | Legible |
|--------|---------|---------|
| `dict_save_json` (3218) / `dict_load_file_json` (3217) | JSON | Sí |
| `dict_save` (3204) / `dict_load_file` (3202) | binario `.wsedict` | No |
| `array_save_file` (5003) / `array_load_file` (5004) | binario `.wsearray` | No |

No existe `str_save_to_file`. JSON es el **único formato legible** que el motor
puede escribir, con valores tipeados y defaults seguros en lectura. Es además
editable a mano por el jugador/modder y autocontenido (todo el árbol en un archivo
con clave de versión).

### Limitación de la v1 (aceptada)

- Sin arrays/anidamiento → esquema plano con claves generadas (0 crecimiento
  "horizontal" de JSON).
- Sin compartición entre máquinas por diseño: los archivos son por-máquina
  (están en la carpeta WSE, no en la partida). Para la v1 está bien.

---

## 5. Flujo de Export

`script_kct_save_tree_to_slot` (`tree_io.py:177-238`), llamado por el botón Export:

1. Nombre = el prefijo del árbol (`cstm_troop_tree_prefix`); "Custom" si vacío.
2. Carga (o crea) el registro de slots.
3. **Auto-asignación de slot**:
   - Si un slot ya tiene el mismo nombre → se **sobrescribe** (rename).
   - Si no, el **primer slot vacío**.
   - Si todos llenos y sin coincidencia → no guarda, mensaje en rojo.
4. `script_kct_export_tree_to_file` empaqueta el árbol en el dict y lo guarda
   como `<prefijo>.json`.
5. Mensaje "Tree saved to slot {n}".

Fuente de verdad: la tropa real (no héroe) para stats/equipo; el dummy (héroe)
para los nombres — el mismo split que usa el Save del store.

---

## 6. Flujo de Import

`script_kct_import_tree_from_file` (`tree_io.py:244-...`), llamado desde la
pantalla de gestión (botón Load):

1. `dict_load_file_json` con el nombre del slot.
2. **Validaciones** (cualquier fallo → mensaje rojo, `reg0 = 0`):
   - `kct_version` debe ser 1.
   - `kct_count` debe coincidir con el nº de tropas del árbol actual
     (`script_kct_compute_tree_range`).
3. Aplica: prefijo, nombre/plural de cada dummy, atributos, habilidades,
   proficiencias, equipo con modificadores, flag de configurado.
4. Sincroniza los dummies y re-equipa su inventario.
5. `reg0 = 1` en éxito → abre el creador con el árbol cargado.

---

## 7. Pantalla de gestión (`prsnt_kct_manage_tree_files`)

- 8 filas con **checkbox + texto + barra dorada** indicando el slot seleccionado.
- Click en fila o checkbox → selecciona (reinicio para redibujar).
- **Load** → importa el slot seleccionado y abre el creador.
- **Delete** → borra `<prefijo>.json` y limpia el slot en el registro
  (`dict_delete_file` + `array_set_val` vacío + `array_save_file`).
- **Exit** → vuelve al picker.
- El registro se autocura en carga (no existe / tamaño incorrecto → recrear).

---

## 8. Distribución al jugador (requisito WSE2)

El mod **requiere WSE2** a partir de ahora (dict_* y array_* no existen ni en
vanilla ni en WSE1). Implicaciones:

- **No hay que empaquetar nada extra**: solo se exporta la carpeta `Modules\<módulo>`.
- Los `.wsearray` / `.json` se crean solos en la carpeta WSE del jugador en su
  primer uso (mecanismo de autocuración, sección 2).
- Son **por-máquina** (no viajan con la partida): si el jugador cambia de PC,
  sus árboles guardados no le siguen. Aceptado para la v1.
- El jugador **no debe** ejecutar el mod sin WSE2 o la persistencia no funciona.

---

## 9. Estado / conclusión

- Export, import y gestión de slots: **implementados y compilando**
  (`python compiler\compile.py tag` → COMPILATION SUCCESSFUL).
- Esquema plano v1, requisito WSE2, sin compartición entre máquinas: **aceptado
  por el usuario**.
- Posibles mejoras futuras (no planificadas): anidamiento real de JSON (si WSE lo
  añade), compartición/exportación de archivos entre PCs, migración de versiones.

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
   **Import** del picker: lista 12 slots (8 seed + 4 usuario), carga o borra árboles guardados.

Persistencia **híbrida opcional** (`kct_scripts/tree_io.py`, `kingdom_custom_troop_tree_creator_constants.py:169`):

- **Vanilla (siempre):** 12 slots en tropas ocultas `trp_kct_template_slot_<n>_meta` + `trp_kct_template_slot_<n>_node_<00-21>` — per-save, sin dependencias. Slots `0-7` seed (6 facciones + Calradian/Falcon), `8-11` usuario.
- **WSE2 (opcional, cross-save):** mismos índices `8-11` usan `dict_*` (3200-3218) → archivos JSON `kct_slot_8.json`..`kct_slot_11.json` en directorio WSE. Si WSE está presente (`neg|is_vanilla_warband 1004`), el wrapper `kct_slot_*` lee/escribe el archivo; si no, cae a vanilla. No hay `array_*` ni `kct trees.wsearray`.

No existe opcode de escritura de texto plano (`str_save_to_file` no existe), así que vanilla usa tropas y WSE usa `dict_save_json`/`dict_load_file_json`.

---

## 2. Dónde se guardan los datos

**Vanilla (per-save):** dentro del `.sav`, en tropas ocultas `trp_kct_template_slot_*` (`kingdom_custom_troop_tree_creator_troops.py:31`, `kct_scripts/tree_io.py:101`). Sin archivos externos. El meta guarda `occupied/tree/gender/count/budget/version` + nombre; cada `node_00..21` guarda una tropa (nombre/plural, 4 att, 42 skl, 7 wpt, equipo+mods, flags).

**WSE2 (cross-save, opcional):** mismos índices `8-11` como JSON externo:
```
Documents\Mount & Blade Warband\WSE\<módulo>\
    ├── kct_slot_8.json   # slot 9 (usuario)
    ├── kct_slot_9.json
    ├── kct_slot_10.json
    └── kct_slot_11.json
```
- Nombre fijo `kct_wse_slot_filename(slot)` (`kingdom_custom_troop_tree_creator_constants.py:185` → `kct_slot_<n>`), sin path (WSE lo resuelve). `storage_path` en `wse_settings.ini` puede moverlo.
- Slots `0-7` seed nunca usan WSE; siempre vanilla.

---

## 3. El registro de slots

Ya no existe `kct trees.wsearray`. El registro es el propio slot:

- Vanilla: `troop_slot_eq meta kct_slot_template_occupied` + `str_store_troop_name meta`.
- WSE: `dict_load_file_json kct_slot_<n>.json` + `neg|dict_is_empty` (`kct_scripts/tree_io.py:347,373`). Vacío = slot libre, con datos = ocupado. No hay array; cada índice es un archivo independiente.

---

## 4. Los datos del árbol

**Vanilla:** `script_kct_export_tree_to_slot` (`tree_io.py:549`) copia del rango live `$cstm_troops_begin..end` a `trp_kct_template_slot_<n>_node_*` vía `_copy_troop_record_ops` (`tree_io.py:101`); `script_kct_import_tree_from_slot` hace el inverso. Todo per-save.

**WSE:** `script_kct_wse_export_tree_to_slot` / `script_kct_wse_import_tree_from_slot` (`tree_io.py:209,261`) hacen lo mismo pero vía `dict_*` JSON `kct_slot_8.json` etc.

### Esquema (JSON plano WSE y vanilla share tool, claves idénticas)

```
kct version   = 1            (int, @kct version)
kct tree      = 0..7         (int, @kct tree — índice preset)
kct gender    = 0..1         (int, @kct gender)
kct budget    = 0..3         (int, @kct budget; 3 = Auto)
kct count     = N            (int, @kct count)
kct prefix    = "Calradian"  (string, @kct prefix)

Por cada tropa i (0..21 máx, solo las N primeras usadas):
  t{i} name        (string, @t{i} name — del dummy)
  t{i} plural      (string, @t{i} plural)
  t{i} att{j}      j=0..3          (@t{i} att{j})
  t{i} skl{j}      j=0..41         (@t{i} skl{j})
  t{i} wpt{j}      j=0..6          (@t{i} wpt{j})
  t{i} eq item{j}  /  t{i} eq mod{j}   j=0..num_equipment_kinds-1
  t{i} conf        (int, @t{i} conf)
  t{i} eqmod       (int, @t{i} eqmod)
  t{i} cls         (int, @t{i} cls)
  t{i} gender      (int, @t{i} gender)
```

`kct_budget` es la clave **aditiva** del presupuesto per-tree (0 Balanced /
1 Boosted / 2 Cheater / 3 Auto), reemplaza la mod-option global `kct_funds_tier`
(eliminada). Se guarda en el slot `cstm_slot_tree_budget_begin + kct_tree` (521–524)
del troop prefijo compartido (`trp_cstm_custom_troops_end`). Por eso `kct_version`
**sigue en 1**: los JSON exportados antes de la clave no tienen `kct_budget` y al
importarlos se asume **Auto (3)** (se adaptan al coste real del equipo, sin denares
gratis).

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

`script_kct_slot_save_tree_auto` (`tree_io.py:800`, wrapper) → `script_kct_save_tree_to_slot` (vanilla) o `script_kct_wse_export_tree_to_slot` (WSE), llamado por el botón Export (`kct_presentations/branch_display.py:395`):

1. Nombre = prefijo (`cstm_troop_tree_prefix`); "Custom" si vacío.
2. **Auto-asignación de slot entre `8-11`** vía wrappers `kct_slot_is_occupied/get_name`:
   - Si un slot ya tiene el mismo nombre → se **sobrescribe**.
   - Si no, el **primer slot vacío**.
   - Si todos llenos → mensaje rojo, no guarda.
3. Wrapper decide backend: `(neg|is_vanilla_warband 1004)` → WSE `dict_create` + `dict_set_*` + `dict_save_json kct_slot_<n>.json`; else vanilla `_copy_troop_record_ops` a `trp_kct_template_slot_<n>_*` + `troop_set_slot meta`.
4. También escribe `@kct budget` (slot `cstm_slot_tree_budget_begin + $cstm_selected_tree`), `gender`, `tree`, `count`, `prefix`.
5. Mensaje "Tree saved to slot {n}" + `kct_import_preview_backup_slot` limpiado.

Fuente de verdad: tropa real para stats/equipo; dummy para nombres.

---

## 6. Flujo de Import

`script_kct_slot_import_tree` (`tree_io.py:820`) → `script_kct_import_tree_from_slot` (vanilla) o `script_kct_wse_import_tree_from_slot` (WSE), llamado desde la pantalla de gestión (Load):

1. Carga: vanilla `troop_get_slot meta` / WSE `dict_create` + `dict_load_file_json kct_slot_<n>.json`.
2. **Validaciones** → rojo `reg0 = 0`:
   - `kct version` == 1, `kct count` == `store_sub $cstm_troops_end $cstm_troops_begin` (`script_kct_compute_tree_range`).
3. Aplica: `kct prefix` → `cstm_troop_tree_prefix` + slot `cstm_slot_tree_budget_begin + kct_tree` (`@kct budget` default 3 Auto), por nodo nombre/plural/att/skl/wpt/eq + `conf/eqmod/cls/gender`, `_copy_troop_record_ops` inverso + `kct_copy_custom_troop_to_dummy`/`kct_replace_custom_troop_with_dummy` + `kct_reapply_all_genders`.
4. Preview backup `kct_import_preview_backup_slot` para deshacer.
5. `reg0 = 1` → abre creador.

---

## 7. Pantalla de gestión (`prsnt_kct_manage_tree_files` — `kct_presentations/tree_files.py`)

- 12 filas (0-11) con **checkbox + texto + barra dorada**; `0-7` seed `Default N:` protegidos, `8-11` usuario `Slot N:`. Estado y nombre vía wrappers `kct_slot_is_occupied`/`kct_slot_get_name` (`tree_files.py:62`).
- Click fila/checkbox → selecciona.
- **Load** → `kct_slot_import_tree` (wrapper).
- **Delete** → `kct_slot_clear` → WSE `dict_delete_file kct_slot_<n>.json` o vanilla `kct_clear_template_slot` (limpia `occupied` + nombres); seed `0-7` bloqueado "Default template slots cannot be deleted".
- **Exit** → picker. Sin autocuración de array (no hay registro).

---

## 8. Distribución al jugador

- **Requisito:** WSE2 **opcional**. Vanilla funciona sin WSE (per-save). Con WSE, mismos `8-11` se vuelven cross-save sin cambiar UI.
- **Empaquetado:** solo `Modules\<módulo>`. Los `kct_slot_*.json` se crean en WSE en el primer Export con WSE; no se distribuyen.
- **Por-máquina cuando WSE:** los JSON no viajan con el `.sav`; cambiar de PC requiere copiar los `kct_slot_*.json` o usar el tool externo `kctt_share_tool` (extract-save → JSON → share) que lee el slot vanilla y produce JSON portable (`vanilla_share_journal.md`).
- **Sin WSE:** no hay archivos; el share es vía savegame + extractor externo.

---

## 9. Estado / conclusión

- Export, import y gestión de slots: **implementados y compilando** (`python compiler\compile.py tag` → COMPILATION SUCCESSFUL). `is_vanilla_warband 1004` decide backend.
- Presupuesto per-tree `@kct budget` (521–524) + `@kct gender` incluidos en esquema; import default budget 3 Auto.
- Esquema plano v1, 12 slots (8 seed + 4 usuario), híbrido vanilla/WSE opcional: **vigente**.
- Futuro: nada planificado; `kctt_share_tool` cubre share sin WSE.

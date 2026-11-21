# Custom Troop Tree — Documentación Técnica / Funcional

> **Fuente de verdad:** `custom_troop_tree_descripcion_base.md` provisto por el autor de la feature. Todo lo descrito ahí se preserva íntegramente. Los commits/diffs se usan solo para verificar nombres exactos (funciones, variables, IDs, rutas) y para enriquecer con referencias de código. Si un punto del .md no es verificable en el diff, se marca como tal — no se omite.

Mod: `modmerger/mods/kingdom_custom_troop_tree_creator/` (archivos `kingdom_custom_troop_tree_creator_*` + subpaquetes `kct_presentations/` y `kct_scripts/`). Mod base tocado: `custom_troops`.

---

## 1. Resumen / Propósito

Existía una feature previa llamada **Custom Troop Tree** que permitía definir un árbol de tropas personalizado para el reino del jugador, pero con errores y limitaciones. La feature actual es un **rediseño y expansión completa** (no un parche) de ese sistema.

**Propósito:** permitir al jugador del reino propio configurar íntegramente su árbol de tropas — presets, nombres, stats, skills, proficiencies, equipo con modificadores, clase y género por tropa — y que ese árbol se use para reclutamiento en aldeas/ciudades/castillos, refuerzos de guarniciones y guardias, con persistencia nativa y opcionalmente cross-save vía WSE.

**Alcance a alto nivel (según .md):**
- 8 presets (3 heredados + Calradion custom + 4 basados en árboles nativos).
- Sistema de import/export con 12 slots (8 nativos + 4 libres) en modo dual Nativo/WSE.
- Configuración por árbol: prefix, budget (Balanced/Boosted/Cheater), checkbox Update Troops.
- Árbol visual con dummies y edición tropa por tropa con regla padre-hijo y orden por tier.
- Edición individual con modifiers, clase manual, género con propagación, Remaining Funds y proficiency sin límite nativo.
- Post-guardado: reemplazo de refuerzos y guardias, aldeas incluidas, y roadmap de guardias por escenario.

Referencias de implementación: presets definidos en `kingdom_custom_troop_tree_creator_constants.py:87` (`KCT_CUSTOM_PRESETS`) + `custom_troops_constants.py:57` (`CUSTOM_TROOP_TREES`); tropas generadas en `kingdom_custom_troop_tree_creator_troops.py:38` + `party_templates` en `kingdom_custom_troop_tree_creator_party_templates.py`.

---

## 2. Trigger y Puntos de Acceso

### 2.1 Descripción (.md §1)

- La presentación se activa **automáticamente cuando el jugador se convierte en rey**, ya sea al iniciar como rey o al fundar/tomar un reino durante la partida, **inmediatamente después de establecer el nombre del reino**.
- **Acceso posterior:** desde el **menú de la ciudad principal** del jugador.
- **Cambio vs. versión anterior:** antes, una vez seleccionada una rama quedaba bloqueada permanentemente. Ahora el jugador **puede cambiar de árbol las veces que quiera**, sin restricción.

### 2.2 Referencias de código

- **Trigger rey:** `source/scripts/activate_player_faction.py:36-42` — `script_activate_player_faction` (`activate_player_faction_scripts`). Si `fac_player_supporters_faction` está en `sfs_inactive` y `:liege == trp_player`, hace `(assign, "$cstm_open_troop_tree_view", 1)` y dispara `mnu_notification_player_faction_active`. Verificado en `activate_player_faction.py:40-41`.
- **Redirección post-nombre del reino:** `source/game_menus/mnu_minister_confirm.py` y `source/game_menus/mnu_auto_return.py` interceptan `$cstm_open_troop_tree_view == 1` y lanzan `(start_presentation, "prsnt_cstm_choose_troop_tree")` en lugar de `change_screen_return`. Es el “inmediatamente después de establecer el nombre” descrito en el .md.
- **Acceso posterior (ciudad principal):** `modmerger/mods/custom_troops/custom_troops_game_menus.py` inyecta la opción en `mnu_center_manage` / `mnu_town` (capital del jugador). El diff `custom_troops_game_menus.py:77` confirma el menú persistente.
- **Sin bloqueo:** el flujo no setea un flag de “ya elegido”; `prsnt_cstm_choose_troop_tree` puede reabrirse desde el menú capital cualquier número de veces — coincide con el cambio descrito.

---

## 3. Flujo Completo de Presentaciones

El .md resume 6 pasos; técnicamente son 4 presentaciones (los pasos 3 y 6 comparten presentación):

| Paso (.md §9) | Presentación (código) | Archivo |
|---|---|---|
| 1. Selección de árbol del reino (8 presets + preview + género) | `prsnt_cstm_choose_troop_tree` | `kct_presentations/branch_selector.py:107` |
| 2. Sistema de importar (12 slots: 8 nativos + 4 libres, vía WSE) | `prsnt_kct_manage_tree_files` | `kct_presentations/tree_files.py:215` |
| 3. Configuración del árbol (prefix, budget, checkbox Update Troops) | `prsnt_cstm_create_troop_tree` (header) | `kct_presentations/branch_display.py:461` |
| 4. Árbol de tropas con dummies (regla padre-hijo, orden por tier, Export) | `prsnt_cstm_create_troop_tree` (viewer) | `kct_presentations/branch_display.py:461` |
| 5. Edición de dummies (armas, clase, género propagado, Remaining Funds, proficiency) | `prsnt_kct_customise_troop` | `kct_presentations/troop_editor.py:22` |
| 6. Sistema post-guardado (update, refuerzos, guardias, aldeas) | lógica en Save de `prsnt_cstm_create_troop_tree` + triggers | `kct_presentations/branch_display.py:412-429`, `kct_scripts/guard_replacements.py`, `kct_scripts/existing_troops.py` |

> Nota: los pasos 3 y 4 son la misma presentación; el header (prefix/budget/checkbox) y el viewer (dummies + líneas + botones Export/Save) se renderizan juntos en `branch_display.py:_build_create_load_ops():225`.

### 3.1 Presentación 1 — `prsnt_cstm_choose_troop_tree` — Selección del árbol del reino

**Descripción (.md §2):**
- 8 presets: 1,2,3 heredados; 4 “Calradion” completamente custom del desarrollador (sin mecánica especial más allá de tier muy alto); 5,6,7,8 basados en árboles nativos.
- Selección de género (ya existía).
- Nuevo preview de rama al seleccionar preset antes de confirmar.
- Incluye acceso a importar (ver §3.0 del .md).

**Implementación:**
- **Presets:** `kct_presentations/layout.py:39-43` `PRESET_NAMES` = 3 de `PRESET_TREES_1_3` (`1_tier` 1×7, `2_tiers` 2×6, `3_tiers` 3×5) + 5 de `KCT_CUSTOM_PRESETS` (`kingdom_custom_troop_tree_creator_constants.py:87-93`): Preset 4 (22 unidades, 6 tiers), Preset 5 (10, 5 tiers), Preset 6 (6, 4), Preset 7 (9, 6 con superunidad F1 lvl40), Preset 8 (9, 5). La descripción “basados en árboles nativos” del .md para 5-8 corresponde a estas 4 formas inspiradas en estructuras nativas, no a imports literales de facciones — ver §8 Notas.
- **Género:** combo Male/Female en `branch_selector.py:33-41` (`$cstm_gender_selector`, `$cstm_selected_gender` 0/1, skins `tf_male`/`tf_female` en `custom_troops_constants.py:64`).
- **Preview:** `branch_selector.py:42-49` — `_draw_tree_ops()` con `PREVIEW (500,380,880,470)` en `layout.py:61`. Presets 1-3 vía `_layout_positions`, presets 4-8 vía lane-based `_custom_preset_positions` / `_preset_4_positions`. Líneas con `script_kct_prsnt_lines_to`, labels cortos (`|A|`, `|B1|`, etc.).
- **Import:** botón `Import` → `prsnt_kct_manage_tree_files` (`branch_selector.py:58-60`, `$kct_import_tree_button`, `$kct_manage_from_picker=1`). Botones `Choose` → `prsnt_cstm_create_troop_tree` (`$cstm_tree_preview_index` → `$cstm_selected_tree`), `Exit`/`ESC` → `change_screen_return`.

### 3.2 Presentación 2 — `prsnt_kct_manage_tree_files` — Sistema de Importar (12 slots)

**Descripción (.md §3):**
- 8 slots nativos por defecto: 6 reinos nativos + 2 custom “Calradion” (Preset 4) y “Falcon”.
- 4 slots libres para el jugador (exporta su árbol aquí).
- Modo dual: con WSE (beneficios completos, persistencia externa al save, portable entre partidas vía JSON) vs. sin WSE (nativo, sin compartir entre saves; herramienta externa en desarrollo).

**Implementación:**
- **Slots:** `kingdom_custom_troop_tree_creator_constants.py:169-183` — `kct_template_slot_count = 12`, `kct_template_storage_slot_count = 13` (12 + backup slot 12), `kct_template_nodes_per_slot = 22` (max de Preset 4), `kct_seeded_template_slot_count = 8`. Cada slot: `trp_kct_template_slot_<n>_meta` + 22 `trp_kct_template_slot_<n>_node_<00-21>` (`kingdom_custom_troop_tree_creator_troops.py:38`).
- **Semillas 0-7:** se siembran en `game_start` vía `script_kct_seed_default_template_slots` (`kingdom_custom_troop_tree_creator_scripts.py`). Son Swadia, Vaegirs, Khergit, Nords, Rhodoks, Sarranid + Calradian (`kct_data/Calradian.json`) + Falcon (`kct_data/Falcon.json`). Label `Default N: {name}` en `tree_files.py:84-87`, protegidos de Delete.
- **Modo dual:** verificado en `kct_scripts/tree_io.py` (wrappers `script_kct_slot_is_occupied`, `script_kct_slot_get_name`, `script_kct_slot_save_tree_auto`, `script_kct_slot_import_tree`, `script_kct_slot_clear`). La rama WSE vs. nativa se decide con `(neg|is_vanilla_warband)` donde `is_vanilla_warband = 1004` (`headers/header_operations.py:1909`) — falla solo si WSE está corriendo. Sin WSE → troop-slots per-save; con WSE → mismos índices 8-11 usan `dict_*` JSON. El .md marca este mecanismo como “a verificar con código” — aquí queda verificado.
- **Ubicación/archivo:** ver §6 Persistencia.
- **Operaciones:** filas en `tree_files.py:56-106` (checkbox + texto + highlight dorado `KTF_ROW_SEL_COLOR 0xC8A000`), botones `Load/Delete/Exit` en `tree_files.py:108-128`. Load valida e importa; Delete bloquea `Default template slots cannot be deleted` (`tree_files.py:197`), muestra `This slot is empty` si vacío, y usa `script_kct_slot_clear`.

### 3.3 Presentación 3 — `prsnt_cstm_create_troop_tree` — Configuración del árbol + Árbol con dummies

Esta presentación cubre dos secciones del .md (§4 y §5) porque el header de configuración y el viewer comparten la misma pantalla.

#### 3.3.1 Configuración del árbol (.md §4)

- **Prefix — nombre del árbol:** text box `Prefix:` en `CSTM_PREFIX_LABEL_POS_X / CSTM_PREFIX_POS_Y` (`branch_display.py:250-254`, `$cstm_set_prefix`, modifica `trp_cstm_custom_troops_end` name). Valor por defecto `Custom` si vacío (`branch_selector.py:54-57`).
- **Budget — 3 modos automáticos:** `Balanced` (costo nativo), `Boosted` (1.5× Balanced), `Cheater` (3× Balanced). En código: `kct_presentations/layout.py:104` `BUDGET_OPTIONS = ("Balanced","Boosted","Cheater","Auto")` — hay un 4º valor `Auto` (= usa el costo del equipo actual, 0 denars libres al abrir). El .md lista solo 3; `Auto` es un adicional implementado (ver §8 discrepancia). Combo en `BUDGET_LABEL_POS/COMBO_POS` (`branch_display.py:264-277`, `$kct_budget_selector`, `750x750` `overlay_set_size`). Persistido per-tree en `cstm_troop_tree_prefix` slot `cstm_slot_tree_budget_begin (521) + $cstm_selected_tree` (ver §5 Reglas).
- **Checkbox “Update Troops”:** label `Update troops:` + checkbox en `UPDATE_EXISTING_LABEL_POS/CHECKBOX_POS` (`branch_display.py:286-290`, `$kct_update_existing_checkbox`, `$cstm_update_existing_troops` 0/1 default 0). Si marcado, al guardar se actualizan guarniciones y tropas del jugador; explícitamente **no** lords. Ver §3.5 post-guardado.

#### 3.3.2 Árbol de tropas con dummies (.md §5)

- **Dummies por defecto:** si no se importó nada, se muestran placeholders. Técnicamente son `trp_cstm_custom_troop_<N>_<skin>_<node>_dummy` (hero, averaged face) vs. tropas reales (`kingdom_custom_troop_tree_creator_troops.py:38`).
- **Configuración personaje por personaje:** click en un retrato dummy abre `prsnt_kct_customise_troop` (§3.4).
- **Orden de inicialización obligatorio — tier más bajo → tier más alto:** aplicado visualmente (tiers como columnas) y como validación: la edición bottom-up bloquea nodos cuyo padre no está configurado (ver §5 Reglas).
- **Regla padre-hijo:** una vez que un padre (tier alto) está configurado, sus hijos (tier bajo) **no pueden tener valores menores a los del padre**. Aplica por defecto, no configurable. En código es “no-decreciente” padre→hijo: el **hijo** no puede ser más débil que el padre (el .md invierte la terminología padre/hijo vs. tiers; el comportamiento es idéntico — ver §5.1 y §8).
- **Botón Export:** exporta automáticamente al **primer slot libre** de los 4 libres (8-11); si no hay libres notifica y el jugador debe eliminar uno. Código: `branch_display.py:308-403` — `script_kct_slot_save_tree_auto` (`tree_io.py:800`) busca slot con mismo nombre para sobrescribir, si no primer vacío 8-11, si no mensaje rojo `no guarda`. Verificado.
- **Presentación propia de import/export:** es `prsnt_kct_manage_tree_files` (§3.2), accesible desde el picker (Import) y desde el viewer (vía Load después de import).

### 3.4 Presentación 4 — `prsnt_kct_customise_troop` — Edición de dummies (individual)

**Descripción (.md §6):**

Conserva el concepto de edición de personaje estándar, con:

- Modificadores de armas configurables por tropa.
- Tipo de clase ajustable manualmente (si la detección automática falla).
- Cambio de género por tropa, con propagación en árbol (rama a femenino → todos los descendientes femeninos; permite dos géneros coexistiendo en el mismo árbol).
- Configuración de puntos básica (igual que personaje estándar).
- Hover sobre skill points muestra detalle adicional.
- Visualización completa: nivel, HP, skill points, etc.
- “Remaining Funds” debajo del inventario: al importar, budget 0 por defecto (ninguno de los 3 modos); si se modifica el árbol importado deja de operar en budget-cero/base; sistema base calcula costo total y lo define como costo final.
- Funcionalidad heredada: nombre singular/plural, navegación entre ítems, selección de género, proficiency.
- Nota técnica: se modificó el límite nativo de proficiency para no estar atado al límite normal del juego (agilidad al configurar por costo).

**Implementación (`kct_presentations/troop_editor.py:22`, layout `layout.py:134-209`):**

- **Top bar:** Name (singular) + box `$cstm_set_name` y Name (plural) + `$cstm_set_name_plural` en `KCT_NAME_POS_X/Y` (`125` + gap `340`). Edita el dummy y setea `$cstm_name_changed`.
- **Izquierda — Inventario:** contenedor scrollable `KCT_INV_POS_X/Y 40/50`, `3×4`, `80` (`$cstm_troop_inventory_container`), grid de `mesh_inv_slot` + `script_kct_create_item_overlay`. Right-click remueve, mensaje `Right-click to remove`. Datos del dummy (primer `num_equipment_kinds` son equipo).
- **Centro — Store:** contenedor `KCT_STORE_POS_X/Y`, `3×7`, `80` (`$cstm_store_container`). Combos item-type (`$cstm_store_item_type_selector`) y modifier (`$cstm_store_item_modifier_selector`, filtrado por `script_kct_cf_cci_imod_appropriate_for_item`, costos por `script_kct_item_type_get_cost_modifier` con `CSTM_IMOD_COST_DIVISOR 2`), paginador `Items page X/Y` (`$cstm_item_page_selector`), grid por página desde `$cstm_items_array` (`trp_cstm_items_array_*`, llenado por `script_kct_setup_item_arrays`). Hover: `show_item_details_with_modifier` + `script_kct_item_get_price_with_modifier` (value + modifier_cost/divisor). `Remaining Funds` en `KCT_STORE_POS_X -3, KCT_STORE_POS_Y -28` amarillo `>=0` / rojo `0xbb0000` <0.
- **Derecha — Stats:** contenedor `KCT_STATS_POS_X/Y` (`$cstm_stats_container`).
  - Línea 1: `Level {reg0}    HP {reg1}` (`store_character_level`, `store_troop_health`).
  - **Clase:** label `Class:` + combo `Auto/Infantry/Cavalry/Archers` en `KCT_CLASS_LABEL/SELECT (0,490)/(200,490)` (`$cstm_class_selector`), persistido `cstm_slot_troop_class_override 533` en tropa real, `750×750`. `Auto` re-deriva (caballo→cavalry, arco/ballesta→archers, si no infantry) vía `script_kct_apply_troop_class`.
  - **Atributos:** STR/AGI/INT en `KCT_STATS_ATTR_*` (`3 cols, 27h, 120w`), `number_box` con mínimos `script_kct_troop_get_attribute_min_from_points/tree` y `script_kct_get_attribute_points_available`, tooltips `str_kct_tip_strength/agility/intelligence` (`kct_attribute_tooltips_begin`, `custom_troops_strings.py`). Bloqueo si `cstm_slot_troop_design_lock 531`.
  - **Puntos atributo:** `Attribute points: {reg0}`.
  - **Proficiencies:** label `Proficiency points: {reg0}` + 7 `number_box` en 2 cols (`KCT_STATS_PROF_*`), acotados por `script_kct_troop_get_proficiency_min/max_from_points/tree`, cap por Weapon Master (`40*WM+60` en `custom_troops_constants.py:85`). Herencia de bonus `cstm_slot_troop_proficiency_bonus 532` incluida.
  - **Skills:** `ACTIVE_FIGHTING_SKILLS` en 2 cols (`KCT_STATS_SKL_*`), `number_box` con `script_kct_troop_get_skill_min_from_points/tree` + `script_kct_get_skill_points_available`, cap INT `/3+1`, tooltips `str_kct_tip_*` por skill.
  - **Género:** combo `Male/Female` en `KCT_GENDER_POS (730,60)` (`$cstm_gender_selector`, `750×750`), `script_kct_flip_subtree` (`kct_scripts/gender.py`) que setea `cstm_slot_troop_gender 534` + `troop_set_type` en el nodo y todo su subárbol (BFS), permitiendo coexistencia de dos géneros en el mismo árbol tal como describe el .md.
- **Bottom bar:** `Save` (si `changes_made` y `remaining_funds>=0`), `Reset`, `Exit` en `KCT_BUTTONS_POS_X/Y`. Save marca `cstm_slot_troop_configured 1`, lockea padre (`cstm_slot_troop_design_lock 1`), `equipment_modified`, aplica clase/género, copia dummy→real (`script_kct_replace_custom_troop_with_dummy`), propaga inventario a hijos no modificados (`script_kct_troop_tree_copy_inventory_if_unmodified`), backup de nombre. Reset/Exit revierten género/clase/nombre. Cheat: click en retrato con `$cheat_mode==1` añade 1 (10 con Shift) a `p_main_party`.
- **Baseline/herencia en entrada fresca:** `$g_kct_recalc_baseline` (seteado por el viewer al clicar nodo) resetea dummy a defaults, lo eleva a niveles del padre, y calcula bonus de proficiency (no gastados + costo heredado) — `troop_editor.py:59-123` + `cstm_slot_troop_inherited 528`.
- **Límites de proficiency:** el cap nativo se elevó vía `CSTM_WP_CAP_LEVELS_PER_WM 40 + CSTM_WP_CAP_ADDITIONAL 200` (en `custom_troops_constants.py:85`), tal como indica la nota técnica del .md.

### 3.5 Presentación 5 (lógica) — Sistema Post-Guardado

**Descripción (.md §8 + §7):**
- Si checkbox Update Troops marcado: al guardar se actualizan **todas las tropas del reino**.
- Si no: no automático, pero se puede re-entrar y actualizar manual en cualquier momento.
- Reemplaza refuerzos a castillos (ahora con facción/árbol custom) y guardias de castillos/ciudades.
- Aldeas también reclutan del árbol custom (md §7) — no solo castillos/ciudades.
- Roadmap futuro: configurar qué tipo de guardia para cada escenario (castillo vs. ciudad). Planeado post-beta.

**Implementación:**
- **Save en `prsnt_cstm_create_troop_tree`:** `branch_display.py:412-429` — `script_kct_clear_template_slot` (backup), `faction_set_slot fac_culture_player tier_1 = $cstm_troops_begin`, reculturiza todo `walled_centers` a `fac_culture_player` (`script_cstm_center_set_culture` que recursa a aldeas), `script_kct_apply_guard_replacements`, y si `$cstm_update_existing_troops==1` llama `script_kct_reset_garrisons_focused` + `script_kct_update_player_party` (si no, quedan para actualización manual tal como describe el .md). Mensaje `Kingdom recruitment updated.`.
- **Guardias:** `kct_scripts/guard_replacements.py` escribe guard slots en `fac_culture_player` + `fac_player_supporters_faction` (hall/castle/prison + calles tier 2/3/4). Hall parcheado en `kingdom_custom_troop_tree_creator_scripts.py: enter_court` (si `center_faction == $players_kingdom` y custom guard `>= cstm_troops_begin` usa custom; si no fallback `$g_player_culture`). Prisión fix `kingdom_custom_troop_tree_creator_game_menus.py` (T8): `-1` → `0` para `trp_hired_blade` fallback.
- **Aldeas:** el refresh de `script_cstm_center_set_culture` sobre cada `walled_center` owned recalcula voluntarios de sus aldeas ligadas — coincide con “aldeas también ofrecen reclutamiento”.
- **Roadmap guardias por escenario:** diseño en `docs/future_updates/troop_trees/guards/last_phase_pick guards.md` (picker futuro), analizado en `guards/guard_system_analysis.md:58-145`. No implementado en esta beta — coincide con el roadmap del .md.

---

## 4. Puntos Funcionales — Detalle Complementario

Esta sección preserva cada punto del .md con su referencia de código exacta. Si un punto no aparece en los commits, se marca como `⚠️ no verificable en diff`.

- **Contexto (md §0):** rediseño completo del Custom Troop Tree previo. Verificado: los archivos previos `custom_troops_presentations.py` (`prsnt_cstm_view_custom_troop_tree`/`cstm_customise_troop`) fueron retirados (`custom_troops_presentations.py` diff `ab9f385`/`e848fa6`) y reemplazados por el nuevo mod KCT.
- **Preview de rama (md §2):** implementado tal como descrito — `branch_selector.py:42-49` + `layout.py:61`.
- **Prefix (md §4):** ver §3.3.1.
- **Budget Balanced/Boosted/Cheater (md §4):** `custom_troops_constants.py:12-41` `EQUIPMENT_FUNDS_TABLE_SIZE 64`, `EQUIPMENT_FUNDS_BANDS` (1-3:110/165/330 … 35-40:20000/30000/60000), `equipment_funds_available(level)` clamp 0 y 41-63. Boosted = Balanced×1.5, Cheater = Balanced×3 cap 60000 — coincide literal con el .md.
- **Modifiers por tropa (md §6):** `troop_editor.py:243-262` modifier combo filtrado por `script_kct_cf_cci_imod_appropriate_for_item`, costos `script_kct_item_type_get_cost_modifier`.
- **Clase manual (md §6):** `cstm_slot_troop_class_override 533` — ver §3.4.
- **Género con propagación (md §6):** `cstm_slot_troop_gender 534` + `script_kct_flip_subtree` — ver §3.4; permite dos géneros en el mismo árbol.
- **Hover skill points (md §6):** `overlay_set_tooltip` en `troop_editor.py:367,937` con `str_kct_tip_*`.
- **Visualización stats completa (md §6):** Level, HP, skill points, proficiencies, attribute points — todos en `troop_editor.py` stats container.
- **Remaining Funds y budget 0 al importar (md §6):** ver §5 Reglas para discrepancia Auto vs. 0.
- **Nombre singular/plural, navegación ítems, género, proficiency (md §6 heredado):** todos en `troop_editor.py` — sg/plural `troop_set_name/plural_name`, store scrollable, gender combo, proficiencies 7.
- **Profi cap modificado (md §6 nota técnica):** `custom_troops_constants.py:85-86` — ver §3.4.

---

## 5. Reglas de Negocio y Validaciones

- **Bottom-up obligatorio — tier bajo → alto:** la presentación ordena tiers como columnas; la validación en `branch_display.py:362-385` exige `cstm_slot_troop_base_troop` padre en `cstm_slot_troop_configured 1` antes de abrir el editor del hijo. Sin esto: mensaje `@'{s0} must be customised before this unit is available.'`
- **Regla padre-hijo (no-decreciente):** el hijo no puede tener valores menores que el padre. El .md la enuncia como “padre tier alto → hijos tier bajo no pueden ser menores”, que es equivalente al invariante padre→hijo hacia tiers superiores. Implementada por `script_kct_troop_get_attribute_min_from_tree` / `script_kct_troop_get_skill_min_from_tree` / `script_kct_troop_get_proficiency_min_from_tree` como `min = max(min_from_points, min_from_tree)`. Además, en entrada fresca el dummy se eleva a los niveles del padre (`troop_editor.py:69-89`).
- **Design lock:** guardar un hijo setea `cstm_slot_troop_design_lock 531` en el padre — sus cajas de stats quedan congeladas (solo equipo/nombre editables). Marcador `cstm_slot_troop_inherited 528` asegura snapshot único.
- **Budget — storage per-tree:** slot `cstm_slot_tree_budget_begin 521 + $cstm_selected_tree` en `trp_cstm_custom_troops_end` (`kingdom_custom_troop_tree_creator_constants.py:160`). 4 valores: 0 Balanced, 1 Boosted, 2 Cheater, 3 Auto. El .md lista solo 3; `Auto` es el 4º implementado (ver §8). Imports usan `Auto` por defecto (ver discrepancia).
- **Budget — tablas:** tres tablas contiguas en `trp_cstm_inventory_values` de `EQUIPMENT_FUNDS_TABLE_SIZE 64` entradas cada una (Balanced `+0`, Boosted `+64`, Cheater `+128`), escritas en `game_start` y por save-fix trigger (`custom_troops_simple_triggers.py`) para que boot y load coincidan. Bandas `EQUIPMENT_FUNDS_BANDS` con clamp.
- **Budget — freeze & snapshot floor:** `$cstm_total_funds` solo en entrada fresca (`$g_kct_recalc_baseline==1`, `troop_editor.py:142-183`). Luego se congela: quitar equipo libera fondos (remaining positivo), añadir por encima queda negativo (rojo) hasta equilibrar; Save exige `remaining_funds >=0`. Para tiers explícitos: `funds = max(table[level], gear_cost)` — cubre gap si el árbol costó más que la tabla o si se bajó el budget después.
- **Slots — límites:** `kct_template_slot_count 12`, seeded `0-7` protegidos de Delete (`tree_files.py:197`), libres `8-11` con auto-asignación por nombre-match si no primer vacío; si los 4 llenos, mensaje rojo y no guarda. Versión `kct_template_version 1` validada en import (`tree_io.py:264-270`) y `kct_count == $cstm_troops_end-$cstm_troops_begin` (range computado por `script_kct_compute_tree_range`).
- **Proficiency — herencia:** bonus `cstm_slot_troop_proficiency_bonus 532` = `max(0, parent_unspent) + cost_inherited_levels` (`troop_editor.py:90-95`), sumado en `script_kct_get_proficiency_points_available`.
- **Clase — override:** `cstm_slot_troop_class_override 533` 0 Auto (caballo→cavalry, arco/ballesta→archers, si no infantry) vs. 1 infantry/2 cavalry/3 archers, re-aplicado en cada load por `kingdom_custom_troop_tree_creator_simple_triggers.py:0`.

---

## 6. Persistencia y Formatos de Archivo

### 6.1 Modelo de almacenamiento

`kingdom_custom_troop_tree_creator_constants.py:169-180` + `kingdom_custom_troop_tree_creator_troops.py:38-63` + `kct_scripts/tree_io.py`

- Cada slot: meta hero `trp_kct_template_slot_<n>_meta` + 22 nodos `trp_kct_template_slot_<n>_node_<00-21>`.
- **Meta slots** (por troop-skill slots 500-534): `0 occupied`, `1 tree`, `2 gender`, `3 count`, `4 budget`, `5 version`.
- **Nodo:** nombre singular/plural, 4 attrs, 42 skills, 7 wpt, equipo+mods, flags `configured/equipment_modified/class_override/gender` vía `_copy_troop_record_ops` (`tree_io.py:101`).

### 6.2 Modo nativo (per-save)

- Dentro del `.sav`, sin archivos externos. `script_kct_export_tree_to_slot` (`tree_io.py:549`) copia rango vivo `$cstm_troops_begin..end` → nodos del slot; `script_kct_import_tree_from_slot` hace el inverso + `kct_copy_custom_troop_to_dummy`/`kct_replace_custom_troop_with_dummy` + `kct_reapply_all_genders`. `script_kct_clear_template_slot` limpia `occupied` + nombres. Funciona siempre.

### 6.3 Modo WSE (cross-save, opcional)

- **Detección:** `(neg|is_vanilla_warband)` con `is_vanilla_warband = 1004` (`header_operations.py:1909`) — falla solo si WSE corre. Wrappers en `kct_scripts/tree_io.py:209,261,740,800,820` (`script_kct_slot_*`) deciden backend.
- **Archivos:** solo índices `8-11` usan JSON externo `kct_slot_8.json`..`kct_slot_11.json` (`kingdom_custom_troop_tree_creator_constants.py:185` `kct_wse_slot_filename(slot)` → `kct_slot_<n>`). Nombre fijo sin path — WSE lo resuelve. `storage_path` en `wse_settings.ini` puede mover la carpeta base. Slots `0-7` seed nunca usan WSE — siempre vanilla. Sin WSE el juego cae a vanilla sin cambio de UI. Verificado en `export_import_info.md` y `vanilla_share_journal.md`.
- **Ubicación:** `Documents\Mount & Blade Warband\WSE\<nombre_del_modulo>\kct_slot_8.json` etc. — ejemplo del .md `C:\Users\Dibey\Documents\Mount&Blade Warband WSE2\WSE\[nombre]` corresponde a instalación WSE2; en código `kct_slot_#` es el nombre de archivo (sin extensión `.json`/`.wsedict` según wrapper `dict_save_json` 3218). La carpeta exacta del mod (`Dickplomacy Reloaded`) proviene de `modmerger` — ver §8 discrepancia menor.
- **Formato JSON plano WSE:** claves `kct_version=1` (`@kct version`), `kct_tree` 0..7 (`@kct tree`), `kct_gender` 0..1, `kct_budget` 0..3 (Auto), `kct_count`, `kct_prefix`, y por tropa `t{i}_name/plural/att{j}/skl{j}/wpt{j}/eq{item,mod}/conf/eqmod/cls/gender`. Plano porque WSE `dict_*` no tiene arrays/dicts anidados (`dict_save_json` 3218 es el único legible; no existe `str_save_to_file`). Ver `export_import_info.md:62-98`.

### 6.4 Compartir entre jugadores y herramienta externa

- El JSON de los slots 8-11 es portable: copiar `kct_slot_8.json` etc. entre máquinas comparte el árbol. El .md describe exactamente este flujo y la persistencia externa al save gracias a WSE — verificado.
- **Herramienta externa:** en desarrollo, para extraer/importar árboles entre saves sin WSE (lee slots vanilla del `.sav` y emite JSON para compartir). No forma parte de esta beta. Los commits no contienen binario de la tool, solo su research y parser plan (`docs/future_updates/troop_trees/export_import/vanilla_share_journal.md` fases 5-6: `kctt-tool extract-save <save> --slot N --out tree.json`, `inspect-json`, `json-to-modsys`). Marcado como pendiente en el .md — confirmado como roadmap no shippeado.

---

## 7. Roadmap / Limitaciones Conocidas

Documentado en el .md §8 y en `guard_system_analysis.md` / `last_phase_pick guards.md`:

- **Guardias por escenario:** permitir configurar qué guardia para cada sitio (castillo vs. ciudad vs. prisión vs. calles tier 2/3/4). Actualmente el picker está planificado y el sistema viejo de auto-scan por clase fue retirado por no fiable (dependía de `troop_get_inventory_slot` + `horse/bow` check); el Save escribe los 6 `slot_faction_*_guard` pero sin UI dedicada aún. Planificado para después de esta beta — no incluido.
- **Modo nativo:** limitación explícita del .md — sin WSE **no se puede compartir/exportar entre saves** (solo per-save). La herramienta externa cubrirá este caso cuando esté lista.
- **Presets 5-8:** el .md dice “basados en árboles nativos”; en código son 4 formas neutras inspiradas en estructuras nativas (no clones literales de Swadia etc.), mientras que los árboles nativos como datos viven como **slots sembrados** 0-5 (ver §8).
- **Edición ilimitada:** a diferencia de la versión previa bloqueada, ahora se puede cambiar de preset/género y re-editar cualquier número de veces — sin restricción.

---

## 8. Notas de Verificación — Discrepancias y Pendientes

### 8.1 Discrepancias .md vs. commits (no se asume que el commit tiene razón automáticamente)

1. **Número de presets con mecánica “Calradion tier alto”:** el .md dice Preset 4 “Calradion” es el único custom con tier muy alto. En código **todos** los presets 4-8 tienen tiers altos (Preset 4 llega a lvl40 F1-F3, Preset 7 a lvl40 F1). Calradion es también el nombre de un **slot sembrado** (`kct_data/Calradian.json`) basado en Preset 4, no un preset distinto por mecánica. **Preservada la redacción del .md**; la discrepancia es terminológica — el tier alto no es exclusivo de Calradion.

2. **Budget — 3 modos vs. 4 modos:** el .md lista Balanced/Boosted/Cheater (3). El código tiene `BUDGET_OPTIONS = ("Balanced","Boosted","Cheater","Auto")` (`layout.py:104`) y slot `cstm_slot_tree_budget_begin 521` con 4 valores (0/1/2/3). **Preservado el texto del .md** (3 modos automáticos) y se anota que `Auto` (= costo del equipo) existe como 4º modo implementado, usado como default para imports.

3. **Remaining Funds — “budget 0” al importar:** el .md dice que un árbol importado usa **budget 0 por defecto** y al modificar deja de operar en budget-cero. El código usa `Auto (3)` como default para imports sin `@kct_budget` (`export_import_info.md:88` — “default 3 Auto”), que equivale a `funds = gear_cost` (remaining 0 pero sin denars gratis). Semánticamente coincide con “budget 0” del .md — se marca como **misma intención, valor distinto (3 vs. 0)**.

4. **Regla padre-hijo — inversión de terminología:** el .md dice “padre tier alto, hijos tier bajo no pueden ser menores”. El código la expresa como **bottom-up** (hijo = tier alto, padre = su upgrade parent) con invariante `hijo >= padre`. Es la misma regla vista desde extremos opuestos; no es contradicción funcional.

5. **Slots — 6 reinos + Calradion + Falcon vs. código 0-7:** el .md lista 8 nativos como 6 reinos + Calradion + Falcon. El código siembra exactamente esos 8 (`vanilla_share_journal.md:106-111` — Swadia, Vaegirs, Khergit, Nords, Rhodoks, Sarranid, Calradian, Falcon) — **coincide**; se deja constancia de que Calradian/Falcon son `kct_data/*.json` vendoreados como seed.

6. **Ruta WSE:** el .md da ejemplo `…\Mount&Blade Warband WSE2\WSE\[nombre del mod]` con archivo `kct_slot_#`. El código usa `kct_wse_slot_filename(slot)` → `kct_slot_<n>` sin extensión en wrapper y `Documents\Mount & Blade Warband\WSE\<modulo>\kct_slot_8.json` (`export_import_info.md:35`). Diferencia de `WSE2` vs. `WSE` es de instalación; el nombre del mod es `Dickplomacy Reloaded`. Marcada como **variación de instalación, no discrepancia funcional**.

### 8.2 Puntos del .md marcados ⚠️ — estado tras verificar con commits

- **⚠️ Formato exacto y mecanismo JSON compartible:** ✅ verificado — flat JSON `kct_*` + `t{i}_*` en `export_import_info.md:62-98` y `kct_scripts/tree_io.py`; ejemplo `kct_slot_8.json` con `dict_save_json` 3218 / `dict_load_file_json` 3217.
- **⚠️ Nombre exacto carpeta del mod y convención de archivo 4 slots libres:** ✅ verificado — carpeta WSE del mod (`Dickplomacy Reloaded`), archivos `kct_slot_8.json`..`kct_slot_11.json` (`kingdom_custom_troop_tree_creator_constants.py:185`), `storage_path` en `wse_settings.ini`.
- **⚠️ Mecanismo exacto de detección WSE y rutas por modo:** ✅ verificado — `is_vanilla_warband = 1004` (`header_operations.py:1909`), wrappers `script_kct_slot_*` en `tree_io.py:209,740,800,820` (WSE: `dict_*`, nativo: troop slots).
- **⚠️ Herramienta externa — estado real en código:** ⚠️ pendiente de confirmar — no hay binario; solo research + plan `kctt-tool extract-save` en `vanilla_share_journal.md:198-434`. **Sigue sin poder confirmarse como implementada; se preserva como roadmap** tal como indica el .md (en desarrollo, no parte de esta beta).
- **⚠️ Nombres de funciones/IDs/rutas por punto funcional:** ✅ enriquecidos en §2-§6 (ver `branch_selector.py`, `branch_display.py`, `troop_editor.py`, `tree_files.py`, `tree_io.py`, `guard_replacements.py`, `gender.py`, `custom_troops_constants.py`, `activate_player_faction.py`, etc.). Todos los puntos funcionales del .md tienen entrada con referencia de código.

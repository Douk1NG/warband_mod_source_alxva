# Al Convertirte en Rey — Configuración de tus Propias Tropas

Requisito del flujo, tal y como lo describió el usuario. Los archivos técnicos y las
fases de implementación los decide el usuario; este documento captura el requisito
para que un agente builder pueda empezar.

## Contexto

- Al convertirte en rey puedes configurar ahora tus propias tropas.
- Las tropas serán reclutables en tus aldeas.
- Los vasallos mantienen las tropas por defecto; las guarniciones igual; tu ejército igual.
- Lo que cambia: tu reino se reconstruye gradualmente con las nuevas unidades.
  Los refuerzos ya no salen de la facción X sino del árbol del jugador.
  Las guarniciones se van reemplazando gradualmente.

## Definición del árbol (primer paso)

1. Hay un **select** que permite escoger entre **4 opciones de ramas** (los 4 presets).
2. Cada opción, al elegirla, muestra una **imagen acorde a la estructura de rama**
   (las imágenes se dibujan proceduralmente con `script_cstm_create_troop_tree_images`;
   no se usan assets externos).
3. Debajo, un botón de **elegir**.
4. Una vez hecho esto, **no hay vuelta atrás**.

## Presentación del árbol

- La presentación tiene el **árbol de ramas** y **botones arriba a la derecha: importar / exportar**.
- El jugador puede **importar plantillas** definidas en la carpeta donde está guardada
  la partida. Al cargar, la rama debe actualizarse con lo cargado.
- **Se guarda automáticamente al salir de la presentación.** Puede que sea necesario
  guardar para arreglar el bug existente de cargar partida (cuando cargas la partida,
  las tropas no están inicializadas).

## Asignación de valores

- Una vez definido el árbol, si no cargaste una plantilla, se va **tropa por tropa
  asignando valores** (la presentación de asignación de valores ya está construida).
- Solo tiene un cambio: **pericia de arma** — en vez de libertad, unos selectores
  que permiten hacerlo automáticamente.
- Pendiente a revisar: la regla de dominio de armas (weapon master) y cómo afecta esto.

---

## Nota técnica: carpeta de las plantillas

Verificado en el código fuente de WSE (`WSELib/WSEOperationContext.cpp`, `CreateStorageDir`):
por defecto `array_save_file` / `array_load_file` guardan en
`Documents\Mount&Blade Warband\WSE\<nombre_del_módulo>\` con extensiones `.wsearray`,
`.wsedict` y `.json`. **No** es la carpeta de la partida
(`Documents\Mount&Blade Warband Savegames\<módulo>\`). La carpeta real se puede fijar
vía `storage_path` en `wse_settings.ini`. Decisión de diseño pendiente del usuario.

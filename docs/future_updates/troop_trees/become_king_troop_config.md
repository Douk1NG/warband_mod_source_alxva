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
4. Acá existirá la **optión de importar** una plantilla de árbol (archivo `.json` o `.wsearray`) que  será cargada en la presentación de asignación de valores. Esto permite que el jugador pueda rápidamente cargar un árbol que ya haya definido previamente, sin tener que volver a definirlo desde cero.

## Presentación del árbol

- La presentación tiene el **árbol de ramas** con sus dummies y labels, un input en el que se establece el pre fijo de tropas, un **selector de presupuesto de equipo** (dropdown "Budget:" debajo del input) y debajo un botón de **exportar** que sirvará para guardar el árbol externamente, además de un botón en la parte superior derecha para salir de la presentación.
- **Se guarda automáticamente al salir de la presentación.**

### Presupuesto de equipo (por árbol)

- Cada árbol lleva su propio presupuesto (ya no hay una opción global en mod options).
- Opciones: **Balanced / Boosted / Cheater** (tablas de niveles) y **Auto** (el
  presupuesto = coste del equipo actual; es el valor por defecto al **importar**
  una plantilla, así cualquier árbol definido antes se adapta sin denares gratis).
- En el store de asignación, el presupuesto se congela al entrar: quitar equipo
  libera dinero y añadir por encima del presupuesto se bloquea (quedando en rojo
  hasta equilibrar).
## Asignación de valores

- Una vez definido el árbol, si no cargaste una plantilla, se va **tropa por tropa
  asignando valores**
- Limites : no se puede tener  una tropa padre con un valor menor que la suma de sus tropas hijas. Esto se valida en tiempo real y se muestra un mensaje de error si se intenta asignar un valor que viole esta regla.

---

## Nota técnica: carpeta de las plantillas

Verificado en el código fuente de WSE (`WSELib/WSEOperationContext.cpp`, `CreateStorageDir`):
por defecto `array_save_file` / `array_load_file` guardan en
`Documents\Mount&Blade Warband\WSE\<nombre_del_módulo>\` con extensiones `.wsearray`,
`.wsedict` y `.json`. **No** es la carpeta de la partida
(`Documents\Mount&Blade Warband Savegames\<módulo>\`). La carpeta real se puede fijar
vía `storage_path` en `wse_settings.ini`. Decisión de diseño pendiente del usuario.

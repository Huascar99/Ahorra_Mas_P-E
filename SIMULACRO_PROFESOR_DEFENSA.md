# Simulacro de Defensa: El Profesor Pregunta (Guía de Supervivencia y Respuestas Ganadoras)

> [!NOTE]
> En este documento actúo como tu **Profesor Evaluador** durante la defensa del proyecto **AhorraMás**. Aquí encontrarás las **12 preguntas con mayor probabilidad de aparecer**, la **respuesta exacta** que debes dar para obtener la máxima calificación, **por qué el profesor hace esa pregunta** (qué está evaluando realmente en silencio) y un **Protocolo de Emergencia** por si te quedas en blanco.

---

## Parte 1: Las 12 Preguntas Más Probables del Profesor

### Pregunta 1: Paradigma de Programación (Sin POO / Sin Clases)
**Profesor:** *"Veo que en todo su proyecto no utilizaron ni una sola clase (`class`). ¿Por qué decidieron trabajar sin Programación Orientada a Objetos y cómo lograron mantener la calidad y el orden del código?"*

- **Por qué te lo pregunta:** Quiere saber si entiendes la diferencia entre **Programación Orientada a Objetos (POO)** y **Programación Estructurada/Modular**, y si sabes justificar técnicamente tu diseño en lugar de decir "porque era más fácil".
- **Tu Respuesta Ganadora:**
  > *"Decidimos aplicar **Programación Estructurada y Modular** con funciones puras y estructuras de datos nativas de Python (listas bidimensionales y diccionarios). Para un sistema financiero transaccional donde los datos entran por peticiones HTTP sin estado (stateless), se validan, se transforman matemáticamente y se guardan en una matriz, usar clases añadía sobrecarga innecesaria de instanciación. Logramos máxima calidad aplicando **Separación de Responsabilidades (SoC)** en módulos independientes (`app.py`, `validaciones.py`, `logica.py`, `persistencia.py`) y el principio **DRY (Don't Repeat Yourself)** reutilizando funciones."*

---

### Pregunta 2: El Uso y Estructura de las Matrices
**Profesor:** *"El sistema menciona que trabaja con un Modelo de Estructura Matricial. Muéstreme en el código dónde están las matrices, qué dimensiones tienen y cómo recorren sus filas y columnas."*

- **Por qué te lo pregunta:** Es el requisito central de estructuras de datos en la interfaz. Quiere comprobar que sabes qué es una matriz en Python (`lista de listas`) y cómo se indexa `[fila][columna]`.
- **Tu Respuesta Ganadora:**
  > *"Implementamos matrices bidimensionales mediante listas anidadas en dos módulos clave:*
  > *1. En `logica.py`, dentro de `calcular_ahorro_anual()`, generamos una **matriz de 12 filas por 3 columnas (`12 x 3`)**, donde cada fila es `[mes, cuota_fija, total_acumulado]`.*
  > *2. En `persistencia.py`, dentro de `cargar_matriz_registros()`, cargamos una **matriz de `N x 5`**, donde cada fila representa un registro y sus 5 columnas son: `[0] ID`, `[1] Titular`, `[2] Tipo de operación`, `[3] Monto` y `[4] Fecha`. En Python accedemos por índice como `fila[0]` y en el HTML la recorremos con un ciclo Jinja2 `{% for fila in matriz_crud %}`."*

---

### Pregunta 3: Persistencia en Archivo de Texto y el Separador `||`
**Profesor:** *"En `persistencia.py` ustedes guardan los registros en `registros.txt` usando `||` (doble barra vertical) para separar las columnas. ¿Por qué usaron `||` y no una simple coma `,` como en un archivo CSV?"*

- **Por qué te lo pregunta:** Quiere evaluar si pensaste en casos de borde (corrupción de datos al hacer `.split()`).
- **Tu Respuesta Ganadora:**
  > *"Porque en un sistema financiero el usuario puede escribir una coma dentro del nombre o del concepto (por ejemplo: `'Juan Pérez, Jr.'` o `'Meta: Laptop, Mouse'`). Si usáramos una coma `,` como delimitador, al hacer `linea.split(',')` esa fila se partiría en 6 o 7 columnas en lugar de 5 y el registro se corrompería. Usando el delimitador compuesto `||` evitamos colisiones con la escritura normal del usuario y además verificamos `if len(columnas) == 5` al cargar la matriz."*

---

### Pregunta 4: Reutilización de Código (Optimización DRY)
**Profesor:** *"Explíqueme cómo optimizaron `logica.py` y `validaciones.py` para no repetir código entre el ahorro mensual y el ahorro anual."*

- **Por qué te lo pregunta:** Quiere ver si realmente optimizaste el código o si solo copiaste y pegaste bloques `if/elif/else`.
- **Tu Respuesta Ganadora:**
  > *"Tanto el ahorro mensual como el ahorro anual evalúan exactamente las mismas reglas financieras (`60/25/15` si gasta $\le 60\%$, `70/20/10` si gasta $< 70\%$, y bloqueo si gasta $\ge 70\%$). En lugar de escribir dos veces esa estructura condicional en `logica.py`, la función `calcular_ahorro_anual()` llama directamente a `calcular_ahorro_mensual()`, toma la cuota de ahorro resultante (`base['ahorro']`) y construye con ella la matriz de 12 meses. Lo mismo hicimos en `validaciones.py`, donde `validar_datos_ahorro_mensual` y `validar_datos_ahorro_anual` reutilizan `validar_datos_gastos`, y `validar_actualizacion_crud` reutiliza `validar_registro_crud`."*

---

### Pregunta 5: El Cálculo del ID en el CRUD
**Profesor:** *"Si tengo 5 registros en el CRUD y elimino el registro #3, ¿qué ID le asigna `crear_registro()` al próximo registro que yo cree y cómo lo calcula?"*

- **Por qué te lo pregunta:** Es una pregunta trampa clásica para ver si usaste `len(matriz) + 1` (que daría error de IDs duplicados) o `max(ids) + 1`.
- **Tu Respuesta Ganadora:**
  > *"Le asignará el **ID #6**. En `crear_registro()` no usamos `len(matriz) + 1` porque al borrar un registro intermedio la longitud disminuye y se repetiría el ID #5. En su lugar, extraemos todos los IDs actuales de la columna `fila[0]` mediante una comprensión de listas `[int(fila[0]) for fila in matriz if fila[0].isdigit()]` y calculamos `max(ids_validos) + 1`. Así garantizamos que el ID sea siempre único y autoincremental."*

---

### Pregunta 6: El Uso de `math.ceil()` en la Meta Indefinida
**Profesor:** *"En `calcular_meta_indefinida()` dentro de `logica.py`, ustedes dividen `meta_dinero / ahorro_mensual` y luego le aplican `math.ceil()`. ¿Por qué `math.ceil()` y no `round()` o `int()`?"*

- **Por qué te lo pregunta:** Evalúa si entiendes la lógica financiera detrás de las funciones matemáticas.
- **Tu Respuesta Ganadora:**
  > *"Porque `int()` trunca los decimales hacia abajo y `round()` redondea hacia abajo si el decimal es menor a `.5`. Si una persona necesita `5.2 meses` para reunir el dinero de una meta y redondeáramos a `5 meses`, al quinto mes le faltaría dinero y no cumpliría su meta. Con `math.ceil()` (función techo) redondeamos siempre al entero superior (`6 meses`), asegurando que en la fecha proyectada el usuario haya completado el 100% del monto objetivo."*

---

### Pregunta 7: Cómo Funciona `calcular_fecha_futura()` sin Librerías Externas
**Profesor:** *"Explíqueme las 3 líneas matemáticas de la función `calcular_fecha_futura(fecha_base, meses)` en `logica.py`. ¿Por qué usan `// 12` y `% 12`?"*

- **Por qué te lo pregunta:** Es la línea matemática más elegante del proyecto. Si la sabes explicar, demuestras dominio total de lógica algorítmica.
- **Tu Respuesta Ganadora:**
  > *"Esa función calcula qué mes y año será dentro de $N$ meses usando **aritmética modular**:*
  > *1. Primero hacemos `total_meses = (fecha_base.month - 1) + meses`. Restamos 1 al mes actual para pasarlo a índice base cero (0 = Enero, 11 = Diciembre).*
  > *2. Luego, con la **división entera** `total_meses // 12` calculamos cuántos años completos de 12 meses han transcurrido y se los sumamos a `fecha_base.year`.*
  > *3. Finalmente, con el **operador módulo** `total_meses % 12` obtenemos el residuo (un número siempre entre 0 y 11), que corresponde a la posición exacta del nuevo mes en la lista `meses_nombres`."*

---

### Pregunta 8: ¿De dónde sale el `30.41` en Meta Definida?
**Profesor:** *"En `calcular_meta_definida()` veo la línea `meses_restantes = dias_restantes / 30.41`. ¿Por qué `30.41` y no `30`?"*

- **Por qué te lo pregunta:** A los profesores les encanta preguntar por constantes numéricas ("números mágicos") para ver si sabes de dónde salieron.
- **Tu Respuesta Ganadora:**
  > *"Porque un año estándar tiene 365 días distribuidos en 12 meses, y $365 / 12 = 30.4166...$ días promedio por mes. Si dividiéramos entre 30 en plazos largos, acumularíamos un desfase de más de 5 días por año. Usar `30.41` ofrece una aproximación mensual mucho más fiel al calendario real."*

---

### Pregunta 9: Validación de Fecha Límite y Prevención de División por Cero
**Profesor:** *"¿Qué ocurre en su sistema si en el módulo de Meta Definida el usuario selecciona la fecha de hoy o una fecha del año pasado?"*

- **Por qué te lo pregunta:** Quiere saber si protegiste la fórmula `costo_meta / dias_restantes` contra un `ZeroDivisionError`.
- **Tu Respuesta Ganadora:**
  > *"El módulo `validaciones.py` lo bloquea antes de llegar a `logica.py`. En `validar_meta_definida()` comparamos `if fecha_limite_valida <= date.today():` y agregamos un error indicando que la fecha límite debe ser estrictamente futura. Esto es vital porque en `logica.py` calculamos `dias_restantes = (fecha_limite_date - date.today()).days` y luego dividimos `costo_meta / dias_restantes`. Si permitiéramos la fecha de hoy, `dias_restantes` sería `0` y provocaría un `ZeroDivisionError`."*

---

### Pregunta 10: Estructuras de Datos Dinámicas sin POO (`arboles.py`, `colas_enlazadas.py`, `grafos.py`)
**Profesor:** *"Normalmente una Cola Enlazada o un Árbol se programan creando una `class Nodo`. ¿Cómo implementaron ustedes los nodos y punteros en `colas_enlazadas.py` y `arboles.py` sin usar clases?"*

- **Por qué te lo pregunta:** Quiere verificar que comprendes cómo se representan nodos y punteros en memoria usando diccionarios en Python.
- **Tu Respuesta Ganadora:**
  > *"En Python los diccionarios son estructuras mutables que se manejan por referencia en memoria. En `colas_enlazadas.py`, la función `crear_nodo(dato)` devuelve el diccionario `{'dato': dato, 'siguiente': None}`, donde la llave `'siguiente'` actúa como puntero al siguiente diccionario nodo. Y la cola es otro diccionario `{'frente': None, 'final': None, 'tamano': 0}` que mantiene las referencias al primer y último nodo para encolar y desencolar en tiempo `O(1)`. De igual manera, en `arboles.py` cada nodo es `{'nombre': nombre, 'hijos': []}`, donde `'hijos'` almacena las referencias a los diccionarios hijos."*

---

### Pregunta 11: Diferencia entre `render_template` y `redirect(url_for(...))` en Flask
**Profesor:** *"En `app.py`, cuando calculan gastos usan `renderizar_panel()` (que llama a `render_template`), pero cuando crean o eliminan un registro en el CRUD usan `redirect(url_for('index', ...))`. ¿Por qué esa diferencia?"*

- **Por qué te lo pregunta:** Evalúa si conoces el patrón web **PRG (Post / Redirect / Get)**.
- **Tu Respuesta Ganadora:**
  > *"Aplicamos el patrón **Post/Redirect/Get (PRG)** en las operaciones del CRUD que modifican el archivo `registros.txt`. Si después de un `POST` a `/crud/crear` respondiéramos directamente con `render_template` y el usuario presionara `F5` (recargar página) en su navegador, el navegador reenviaría la petición `POST` y **crearía el mismo registro duplicado otra vez**. Al responder con `redirect(url_for('index', seccion='crud'))`, convertimos la navegación final en una petición `GET` limpia y segura."*

---

### Pregunta 12: ¿Por qué crearon la función `renderizar_panel` en `app.py`?
**Profesor:** *"En `app.py` tienen una función `renderizar_panel(...)` que usa `**kwargs`. ¿Qué hace esa función y por qué usaron `**kwargs`?"*

- **Por qué te lo pregunta:** Es una de las mejores optimizaciones en `app.py` y el uso de `**kwargs` llama la atención del evaluador.
- **Tu Respuesta Ganadora:**
  > *"La creamos para eliminar código repetido en `app.py`. Como nuestra interfaz está unificada en una sola plantilla `index.html`, todas las rutas necesitan enviarle siempre la `seccion_activa`, `subseccion_activa`, `form_data` y la `matriz_crud` actualizada desde `persistencia`. En lugar de repetir esas 5 líneas en las 11 funciones de `app.py`, `renderizar_panel()` las carga automáticamente y usa `**kwargs` (argumentos variables por palabra clave) para recibir cualquier resultado específico de cada módulo (como `resultado_gastos`, `resultado_ahorro_anual` o `errores`) y pasárselo a `render_template`."*

---

## Parte 2: ¿Qué Hacer Si Te Quedas en Blanco Durante la Defensa? (Protocolo de Rescate)

Quedarse en blanco por los nervios es completamente normal. Si el profesor te hace una pregunta y sientes que la mente se te bloquea, **nunca te quedes callado mirando al suelo ni digas "no sé"**. Aplica estas **4 técnicas de rescate inmediato**:

### Técnica 1: "Anclaje en el Flujo de 3 Capas" (Para ganar 10 segundos y reactivar tu memoria)
Cualquier pregunta sobre el funcionamiento del sistema pasa siempre por las mismas 3 capas. Si te quedas en blanco, empieza diciendo con calma:
> *"Para responderle con precisión, permítame ubicarlo dentro del flujo de nuestras tres capas: primero el dato entra por la ruta en `app.py`, pasa por el filtro de `validaciones.py` y luego se procesa en `logica.py` (o `persistencia.py`)..."*

Mientras dices esa frase (que siempre es cierta en tu proyecto), tu cerebro baja la ansiedad y recuerda en cuál de los 3 archivos está la respuesta.

### Técnica 2: "Apóyate en el Código en Pantalla" (Usa los nombres autoexplicativos)
No tienes que responder de memoria con los ojos cerrados; tienes derecho a abrir el archivo. Di:
> *"Permítame abrir la función en el módulo correspondiente para mostrárselo directamente sobre la línea de código."*

Como optimizamos el código para que cada función tenga entre 5 y 25 líneas y nombres totalmente descriptivos (`validar_numero_positivo`, `cargar_matriz_registros`, `calcular_fecha_futura`), **apenas veas las 4 o 5 líneas en pantalla recordarás qué hace**.

### Técnica 3: "Desglose Entrada $\rightarrow$ Proceso $\rightarrow$ Salida"
Si el profesor señala una función específica y te bloqueas, no intentes explicarla de golpe. Explícala en 3 pasos mecánicos mirando la función:
1. **Mira los paréntesis `def funcion(a, b):`** y di: *"Primero, esta función recibe como entrada los parámetros `a` y `b`..."*
2. **Mira el `if` o el `for` del centro** y di: *"Segundo, valida/recorre estos datos para calcular..."*
3. **Mira el `return`** y di: *"Y finalmente retorna este diccionario/lista hacia `app.py` para mostrarlo en la vista."*

### Técnica 4: Qué responder si te pide algo que el sistema NO tiene (ej. Base de Datos SQL o Login de Usuarios)
Si el profesor pregunta *"¿Por qué no usaron SQLite/MySQL?"* o *"¿Qué pasa si dos usuarios entran al mismo tiempo?"*, no te pongas a la defensiva. Responde con elegancia académica:
> *"Para el alcance académico de este proyecto priorizamos demostrar el dominio algorítmico de **matrices bidimensionales en memoria y persistencia en archivos planos secuenciales (`registros.txt`)** sin depender de motores externos. Sin embargo, gracias a que aislamos toda la lectura y escritura en `persistencia.py`, si en una siguiente versión quisiéramos migrar a SQLite o PostgreSQL, **solo tendríamos que modificar `persistencia.py`** sin tocar ni una sola línea de `app.py`, `logica.py` ni `validaciones.py`."*

*(Esa respuesta demuestra que entiendes **Arquitectura Modular y Desacoplamiento**, lo cual impresiona a cualquier profesor de Ingeniería de Sistemas).*

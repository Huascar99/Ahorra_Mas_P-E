import os
from datetime import datetime

NOMBRE_ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "registros.txt")


# ==============================================================================
# FUNCIÓN: cargar_matriz_registros
# - QUÉ HACE: Lee el archivo de texto `registros.txt` línea por línea, separa
#   cada línea mediante el delimitador `||` y construye una matriz bidimensional
#   (lista de listas) donde cada fila tiene 5 columnas: [ID, Titular, Tipo, Monto, Fecha].
# - POR QUÉ LO HACE: Porque el archivo plano guarda texto secuencial en disco y
#   necesitamos transformarlo en una matriz `[fila][columna]` en memoria RAM
#   para poder recorrerlo, mostrarlo en tablas HTML y manipularlo en Python.
# - PARA QUÉ SIRVE: Para recuperar los datos guardados cada vez que se consulta
#   o modifica el panel CRUD sin depender de motores de bases de datos externos.
# ==============================================================================
def cargar_matriz_registros():
    matriz_registros = []
    if not os.path.exists(NOMBRE_ARCHIVO):
        return matriz_registros

    with open(NOMBRE_ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("||")
            if len(columnas) == 5:
                matriz_registros.append(columnas)
    return matriz_registros


# ==============================================================================
# FUNCIÓN: guardar_matriz_registros
# - QUÉ HACE: Recibe la matriz bidimensional de registros en memoria y la
#   escribe completa en el archivo `registros.txt`, uniendo las 5 columnas de
#   cada fila con el separador `||`.
# - POR QUÉ LO HACE: Porque los cambios hechos en listas de Python viven en la
#   memoria RAM volátil; al volcarlos a disco duro aseguramos persistencia real
#   aunque se apague el servidor Flask.
# - PARA QUÉ SIRVE: Para sincronizar el estado de la matriz en memoria con el
#   archivo físico después de crear, editar, eliminar o vaciar registros.
# ==============================================================================
def guardar_matriz_registros(matriz_registros):
    with open(NOMBRE_ARCHIVO, "w", encoding="utf-8") as archivo:
        for fila in matriz_registros:
            archivo.write("||".join(str(campo) for campo in fila) + "\n")


# ==============================================================================
# FUNCIÓN: obtener_todos_los_registros
# - QUÉ HACE: Devuelve la matriz completa de registros almacenados llamando a
#   `cargar_matriz_registros()`.
# - POR QUÉ LO HACE: Para ofrecer una función de lectura (Read del CRUD) con
#   nombre semántico claro hacia el controlador `app.py`.
# - PARA QUÉ SIRVE: Para abastecer de datos a la tabla del Panel CRUD y al
#   contador de registros del Dashboard en la interfaz web.
# ==============================================================================
def obtener_todos_los_registros():
    return cargar_matriz_registros()


# ==============================================================================
# FUNCIÓN: crear_registro
# - QUÉ HACE: Calcula el siguiente ID numérico autoincremental disponible,
#   genera la marca de tiempo actual, ensambla una nueva fila de 5 columnas
#   `[id, nombre, tipo, monto, fecha]` y la añade al final de la matriz.
# - POR QUÉ LO HACE: Porque cada registro en el CRUD necesita un identificador
#   único irrepetible (`max(ids) + 1`) para poder ser editado o eliminado
#   posteriormente sin confusiones.
# - PARA QUÉ SIRVE: Para implementar la operación Create (Alta) del CRUD tanto
#   desde el botón manual como desde los botones de guardado de cada módulo.
# ==============================================================================
def crear_registro(nombre, tipo, monto):
    matriz = cargar_matriz_registros()
    ids_validos = [int(fila[0]) for fila in matriz if fila[0].isdigit()]
    nuevo_id = max(ids_validos) + 1 if ids_validos else 1

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nueva_fila = [
        str(nuevo_id),
        str(nombre).strip(),
        str(tipo).strip(),
        f"{float(monto):.2f}",
        fecha_actual
    ]
    matriz.append(nueva_fila)
    guardar_matriz_registros(matriz)
    return nueva_fila


# ==============================================================================
# FUNCIÓN: obtener_registro_por_id
# - QUÉ HACE: Recorre las filas de la matriz buscando aquella cuya columna `[0]`
#   coincida con el `id_registro` solicitado y la retorna (o `None` si no existe).
# - POR QUÉ LO HACE: Porque en una matriz indexada es necesario un recorrido
#   lineal por la primera columna para localizar un elemento específico por clave.
# - PARA QUÉ SIRVE: Para consultar los datos de una fila puntual cuando se
#   requiere verificar su existencia o inspeccionar su contenido.
# ==============================================================================
def obtener_registro_por_id(id_registro):
    id_busqueda = str(id_registro).strip()
    for fila in cargar_matriz_registros():
        if fila[0] == id_busqueda:
            return fila
    return None


# ==============================================================================
# FUNCIÓN: actualizar_registro
# - QUÉ HACE: Busca en la matriz la fila cuyo ID (`fila[0]`) coincida con
#   `id_registro`, reemplaza sus columnas de nombre `[1]`, tipo `[2]`, monto `[3]`
#   y fecha `[4]`, y guarda la matriz actualizada en el archivo.
# - POR QUÉ LO HACE: Porque la operación Update del CRUD debe modificar
#   únicamente las celdas de la fila seleccionada conservando intacto su ID
#   original y el resto de filas de la matriz.
# - PARA QUÉ SIRVE: Para permitir al usuario corregir o actualizar montos,
#   nombres o tipos de operación desde la ventana modal de edición.
# ==============================================================================
def actualizar_registro(id_registro, nuevo_nombre, nuevo_tipo, nuevo_monto):
    matriz = cargar_matriz_registros()
    id_busqueda = str(id_registro).strip()

    for fila in matriz:
        if fila[0] == id_busqueda:
            fila[1] = str(nuevo_nombre).strip()
            fila[2] = str(nuevo_tipo).strip()
            fila[3] = f"{float(nuevo_monto):.2f}"
            fila[4] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            guardar_matriz_registros(matriz)
            return True
    return False


# ==============================================================================
# FUNCIÓN: eliminar_registro
# - QUÉ HACE: Filtra la matriz conservando únicamente las filas cuyo ID sea
#   distinto al `id_registro` indicado y sobrescribe el archivo si hubo cambios.
# - POR QUÉ LO HACE: Porque al construir una nueva matriz sin la fila
#   seleccionada se elimina el registro de forma limpia y atómica sin dejar
#   líneas vacías en el archivo de texto.
# - PARA QUÉ SIRVE: Para ejecutar la operación Delete (Baja individual) cuando
#   el usuario pulsa el botón de papelera en una fila del Panel CRUD.
# ==============================================================================
def eliminar_registro(id_registro):
    matriz = cargar_matriz_registros()
    id_busqueda = str(id_registro).strip()
    matriz_filtrada = [fila for fila in matriz if fila[0] != id_busqueda]

    if len(matriz_filtrada) == len(matriz):
        return False

    guardar_matriz_registros(matriz_filtrada)
    return True


# ==============================================================================
# FUNCIÓN: eliminar_todos_los_registros
# - QUÉ HACE: Sobrescribe el archivo de persistencia con una matriz vacía `[]`.
# - POR QUÉ LO HACE: Para reiniciar por completo el almacén de datos en una
#   sola operación de escritura en disco.
# - PARA QUÉ SIRVE: Para dar soporte al botón "Vaciar Todo" del Panel CRUD.
# ==============================================================================
def eliminar_todos_los_registros():
    guardar_matriz_registros([])
    return True

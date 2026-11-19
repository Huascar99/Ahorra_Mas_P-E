from pathlib import Path
from datetime import datetime

CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_REGISTROS = CARPETA_PROYECTO / "registros.txt"
RUTA_OPERACIONES = CARPETA_PROYECTO / "datos" / "operaciones.txt"


# ==============================================================================
# FUNCIÓN: asegurar_archivo
# - QUÉ HACE: Recibe una ruta de archivo, crea sus carpetas contenedoras si no
#   existen y crea el archivo vacío si aún no ha sido creado.
# - POR QUÉ LO HACE: Para evitar errores `FileNotFoundError` al intentar leer
#   o escribir registros u operaciones por primera vez.
# - PARA QUÉ SIRVE: Para preparar de forma segura cualquier archivo plano en
#   disco antes de operar sobre él, sin usar constructores de clases (`__init__`).
# ==============================================================================
def asegurar_archivo(ruta):
    ruta_obj = Path(ruta)
    ruta_obj.parent.mkdir(parents=True, exist_ok=True)
    if not ruta_obj.exists():
        ruta_obj.touch()
    return ruta_obj


# ==============================================================================
# FUNCIÓN: leer_registros_archivo
# - QUÉ HACE: Abre el archivo de registros, lee todas las líneas no vacías,
#   las divide por el separador `||` y devuelve una matriz (lista de listas)
#   con las filas de 5 columnas válidas.
# - POR QUÉ LO HACE: Para cargar los datos tabulares del archivo plano a una
#   estructura matricial manipulable en Python de forma 100% procedimental.
# - PARA QUÉ SIRVE: Para consultar todos los registros almacenados en disco.
# ==============================================================================
def leer_registros_archivo(ruta=RUTA_REGISTROS):
    ruta_obj = asegurar_archivo(ruta)
    registros = []
    with open(ruta_obj, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("||")
            if len(columnas) == 5:
                registros.append(columnas)
    return registros


# ==============================================================================
# FUNCIÓN: guardar_registros_archivo
# - QUÉ HACE: Sobrescribe el archivo plano con todas las filas de la matriz
#   `registros`, uniendo cada campo con el separador `||`.
# - POR QUÉ LO HACE: Para persistir en almacenamiento secundario cualquier
#   modificación o eliminación realizada sobre la matriz en memoria.
# - PARA QUÉ SIRVE: Para guardar el estado completo de la matriz de registros.
# ==============================================================================
def guardar_registros_archivo(registros, ruta=RUTA_REGISTROS):
    ruta_obj = asegurar_archivo(ruta)
    with open(ruta_obj, "w", encoding="utf-8") as archivo:
        for registro in registros:
            archivo.write("||".join(str(campo) for campo in registro) + "\n")


# ==============================================================================
# FUNCIÓN: agregar_registro_archivo
# - QUÉ HACE: Abre el archivo en modo adición (`"a"` - append) e inserta una
#   nueva fila al final sin necesidad de reescribir todo el archivo.
# - POR QUÉ LO HACE: Porque el modo `"a"` posiciona el puntero directamente al
#   final del archivo, haciendo la inserción de un registro nuevo mucho más
#   rápida (`O(1)`).
# - PARA QUÉ SIRVE: Para añadir rápidamente un nuevo registro al archivo.
# ==============================================================================
def agregar_registro_archivo(registro, ruta=RUTA_REGISTROS):
    ruta_obj = asegurar_archivo(ruta)
    with open(ruta_obj, "a", encoding="utf-8") as archivo:
        archivo.write("||".join(str(campo) for campo in registro) + "\n")


# ==============================================================================
# FUNCIÓN: buscar_registro_archivo
# - QUÉ HACE: Recorre los registros del archivo y retorna la fila cuyo primer
#   elemento (`registro[0]`, el ID) coincida con `id_registro`.
# - POR QUÉ LO HACE: Para localizar un registro específico mediante búsqueda
#   secuencial por su clave primaria.
# - PARA QUÉ SIRVE: Para recuperar los datos de un único registro a partir de
#   su identificador.
# ==============================================================================
def buscar_registro_archivo(id_registro, ruta=RUTA_REGISTROS):
    id_str = str(id_registro).strip()
    for registro in leer_registros_archivo(ruta):
        if registro[0] == id_str:
            return registro
    return None


# ==============================================================================
# FUNCIÓN: eliminar_registro_archivo
# - QUÉ HACE: Lee todos los registros, filtra fuera aquel cuyo ID coincida con
#   `id_registro` y guarda la matriz resultante si se encontró y eliminó.
# - POR QUÉ LO HACE: Porque en archivos de texto secuenciales la forma limpia
#   de borrar una línea intermedia es reescribir las líneas que sí permanecen.
# - PARA QUÉ SIRVE: Para dar de baja un registro específico del archivo plano.
# ==============================================================================
def eliminar_registro_archivo(id_registro, ruta=RUTA_REGISTROS):
    registros = leer_registros_archivo(ruta)
    id_str = str(id_registro).strip()
    nuevos = [reg for reg in registros if reg[0] != id_str]

    if len(nuevos) == len(registros):
        return False

    guardar_registros_archivo(nuevos, ruta)
    return True


# ==============================================================================
# FUNCIÓN: registrar_operacion_historial
# - QUÉ HACE: Escribe una línea de bitácora con la fecha/hora actual y la
#   descripción de la `operacion` en el archivo `operaciones.txt`.
# - POR QUÉ LO HACE: Para llevar una auditoría cronológica de las acciones
#   realizadas en el sistema financiero.
# - PARA QUÉ SIRVE: Para guardar el historial de operaciones en disco.
# ==============================================================================
def registrar_operacion_historial(operacion, ruta=RUTA_OPERACIONES):
    ruta_obj = asegurar_archivo(ruta)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ruta_obj, "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha}||{operacion}\n")


# ==============================================================================
# FUNCIÓN: consultar_operaciones_historial
# - QUÉ HACE: Lee el archivo `operaciones.txt` y devuelve una lista con todas
#   las líneas registradas en la bitácora.
# - POR QUÉ LO HACE: Para recuperar el historial de auditoría almacenado en
#   texto plano sin líneas en blanco.
# - PARA QUÉ SIRVE: Para visualizar las operaciones históricas del sistema.
# ==============================================================================
def consultar_operaciones_historial(ruta=RUTA_OPERACIONES):
    ruta_obj = asegurar_archivo(ruta)
    with open(ruta_obj, "r", encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]

from pathlib import Path
from datetime import datetime

CARPETA_PROYECTO = Path(__file__).resolve().parent
RUTA_REGISTROS = CARPETA_PROYECTO / "registros.txt"
RUTA_OPERACIONES = CARPETA_PROYECTO / "datos" / "operaciones.txt"


def asegurar_archivo(ruta):
    ruta_obj = Path(ruta)
    ruta_obj.parent.mkdir(parents=True, exist_ok=True)
    if not ruta_obj.exists():
        ruta_obj.touch()
    return ruta_obj


def leer_registros_archivo(ruta=RUTA_REGISTROS):
    ruta_obj = asegurar_archivo(ruta)
    registros = []
    with open(ruta_obj, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("||")
            if len(columnas) == 5:
                registros.append(columnas)
    return registros


def guardar_registros_archivo(registros, ruta=RUTA_REGISTROS):
    ruta_obj = asegurar_archivo(ruta)
    with open(ruta_obj, "w", encoding="utf-8") as archivo:
        for registro in registros:
            archivo.write("||".join(str(campo) for campo in registro) + "\n")


def agregar_registro_archivo(registro, ruta=RUTA_REGISTROS):
    ruta_obj = asegurar_archivo(ruta)
    with open(ruta_obj, "a", encoding="utf-8") as archivo:
        archivo.write("||".join(str(campo) for campo in registro) + "\n")


def buscar_registro_archivo(id_registro, ruta=RUTA_REGISTROS):
    id_str = str(id_registro).strip()
    for registro in leer_registros_archivo(ruta):
        if registro[0] == id_str:
            return registro
    return None


def eliminar_registro_archivo(id_registro, ruta=RUTA_REGISTROS):
    registros = leer_registros_archivo(ruta)
    id_str = str(id_registro).strip()
    nuevos = [reg for reg in registros if reg[0] != id_str]

    if len(nuevos) == len(registros):
        return False

    guardar_registros_archivo(nuevos, ruta)
    return True


def registrar_operacion_historial(operacion, ruta=RUTA_OPERACIONES):
    ruta_obj = asegurar_archivo(ruta)
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ruta_obj, "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha}||{operacion}\n")


def consultar_operaciones_historial(ruta=RUTA_OPERACIONES):
    ruta_obj = asegurar_archivo(ruta)
    with open(ruta_obj, "r", encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]

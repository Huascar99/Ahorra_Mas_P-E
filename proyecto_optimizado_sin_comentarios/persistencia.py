import os
from datetime import datetime

NOMBRE_ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "registros.txt")


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


def guardar_matriz_registros(matriz_registros):
    with open(NOMBRE_ARCHIVO, "w", encoding="utf-8") as archivo:
        for fila in matriz_registros:
            archivo.write("||".join(str(campo) for campo in fila) + "\n")


def obtener_todos_los_registros():
    return cargar_matriz_registros()


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


def obtener_registro_por_id(id_registro):
    id_busqueda = str(id_registro).strip()
    for fila in cargar_matriz_registros():
        if fila[0] == id_busqueda:
            return fila
    return None


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


def eliminar_registro(id_registro):
    matriz = cargar_matriz_registros()
    id_busqueda = str(id_registro).strip()
    matriz_filtrada = [fila for fila in matriz if fila[0] != id_busqueda]

    if len(matriz_filtrada) == len(matriz):
        return False

    guardar_matriz_registros(matriz_filtrada)
    return True


def eliminar_todos_los_registros():
    guardar_matriz_registros([])
    return True

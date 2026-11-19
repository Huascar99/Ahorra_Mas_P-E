# ==============================================================================
# MÓDULO: listas.py (100% Estructurado / Sin Clases ni POO)
# Operaciones de gestión, búsqueda, filtrado y ordenamiento sobre listas
# dinámicas de diccionarios financieros en memoria.
# ==============================================================================


# ==============================================================================
# FUNCIÓN: crear_lista
# - QUÉ HACE: Crea y retorna una lista vacía `[]`.
# - POR QUÉ LO HACE: Para inicializar una colección secuencial en memoria sin
#   recurrir a una clase envolvente (`class ListaFinanciera`).
# - PARA QUÉ SIRVE: Para almacenar registros financieros en memoria RAM.
# ==============================================================================
def crear_lista():
    return []


# ==============================================================================
# FUNCIÓN: agregar_elemento
# - QUÉ HACE: Inserta un diccionario `registro` al final de la `lista`.
# - POR QUÉ LO HACE: Porque `.append()` en Python agrega elementos al final del
#   arreglo dinámico en tiempo amortizado constante `O(1)`.
# - PARA QUÉ SIRVE: Para registrar un nuevo movimiento en la lista financiera.
# ==============================================================================
def agregar_elemento(lista, registro):
    lista.append(registro)
    return True


# ==============================================================================
# FUNCIÓN: mostrar_lista
# - QUÉ HACE: Devuelve una copia superficial de la `lista` de registros.
# - POR QUÉ LO HACE: Para proteger la lista original frente a modificaciones
#   externas accidentales durante su lectura.
# - PARA QUÉ SIRVE: Para consultar todos los elementos actuales de la lista.
# ==============================================================================
def mostrar_lista(lista):
    return lista.copy()


# ==============================================================================
# FUNCIÓN: buscar_por_id
# - QUÉ HACE: Recorre la `lista` comparando el campo `"id"` de cada registro
#   con `id_registro` y retorna el diccionario encontrado (o `None`).
# - POR QUÉ LO HACE: Realiza una búsqueda lineal `O(n)` convirtiendo ambos IDs
#   a texto para evitar fallos por diferencias de tipo (`int` vs `str`).
# - PARA QUÉ SIRVE: Para localizar un movimiento financiero específico por ID.
# ==============================================================================
def buscar_por_id(lista, id_registro):
    id_str = str(id_registro)
    for registro in lista:
        if str(registro.get("id")) == id_str:
            return registro
    return None


# ==============================================================================
# FUNCIÓN: actualizar_elemento
# - QUÉ HACE: Localiza un registro por `id_registro` usando `buscar_por_id` y,
#   si existe, actualiza sus claves con el diccionario `nuevos_datos`.
# - POR QUÉ LO HACE: Porque como los diccionarios en Python son mutables por
#   referencia, `.update()` modifica directamente el registro dentro de la lista.
# - PARA QUÉ SIRVE: Para editar los campos de un elemento existente en la lista.
# ==============================================================================
def actualizar_elemento(lista, id_registro, nuevos_datos):
    registro = buscar_por_id(lista, id_registro)
    if registro is None:
        return False
    registro.update(nuevos_datos)
    return True


# ==============================================================================
# FUNCIÓN: eliminar_elemento
# - QUÉ HACE: Busca la posición (índice) del registro cuyo `"id"` coincida con
#   `id_registro` y lo extrae de la lista con `.pop(indice)`.
# - POR QUÉ LO HACE: Usar `enumerate` junto con `.pop()` detiene el recorrido
#   apenas encuentra el elemento y desplaza los elementos restantes sin crear
#   listas adicionales.
# - PARA QUÉ SIRVE: Para borrar un registro específico de la lista por su ID.
# ==============================================================================
def eliminar_elemento(lista, id_registro):
    id_str = str(id_registro)
    for posicion, registro in enumerate(lista):
        if str(registro.get("id")) == id_str:
            lista.pop(posicion)
            return True
    return False


# ==============================================================================
# FUNCIÓN: filtrar_por_tipo
# - QUÉ HACE: Retorna una nueva lista con todos los registros cuyo campo
#   `"tipo"` coincida (ignorando mayúsculas/minúsculas) con el `tipo` buscado.
# - POR QUÉ LO HACE: Mediante comprensión de listas (`list comprehension`)
#   selecciona en una sola expresión todos los movimientos de una categoría.
# - PARA QUÉ SIRVE: Para separar registros por tipo (ej. solo "Ahorro Mensual").
# ==============================================================================
def filtrar_por_tipo(lista, tipo):
    tipo_buscado = tipo.lower()
    return [reg for reg in lista if reg.get("tipo", "").lower() == tipo_buscado]


# ==============================================================================
# FUNCIÓN: ordenar_por_monto
# - QUÉ HACE: Devuelve una nueva lista con los registros ordenados de menor a
#   mayor según su campo numérico `"monto"`.
# - POR QUÉ LO HACE: Usa el algoritmo Timsort nativo de Python (`sorted`,
#   complejidad `O(n log n)`) extrayendo el monto como `float` mediante una
#   función auxiliar `obtener_monto_numerico`.
# - PARA QUÉ SIRVE: Para clasificar los registros financieros desde el monto
#   más pequeño hasta el más alto.
# ==============================================================================
def obtener_monto_numerico(registro):
    return float(registro.get("monto", 0))


def ordenar_por_monto(lista):
    return sorted(lista, key=obtener_monto_numerico)


# ==============================================================================
# FUNCIÓN: cantidad_elementos
# - QUÉ HACE: Retorna la cantidad total de elementos en la `lista` con `len()`.
# - POR QUÉ LO HACE: `len()` en listas de Python opera en tiempo constante `O(1)`.
# - PARA QUÉ SIRVE: Para saber cuántos registros hay cargados en la lista.
# ==============================================================================
def cantidad_elementos(lista):
    return len(lista)


# ==============================================================================
# FUNCIÓN: lista_vacia
# - QUÉ HACE: Devuelve `True` si la lista no tiene elementos (`len(lista) == 0`).
# - POR QUÉ LO HACE: Para comprobar rápidamente si existen datos antes de
#   ejecutar reportes o recorridos.
# - PARA QUÉ SIRVE: Para verificar si la estructura lineal está vacía.
# ==============================================================================
def lista_vacia(lista):
    return len(lista) == 0


# ==============================================================================
# FUNCIÓN: limpiar_lista
# - QUÉ HACE: Elimina todos los elementos de la `lista` in-situ con `.clear()`.
# - POR QUÉ LO HACE: Para vaciar la misma lista en memoria sin perder su
#   referencia original.
# - PARA QUÉ SIRVE: Para reiniciar la lista financiera a cero elementos.
# ==============================================================================
def limpiar_lista(lista):
    lista.clear()

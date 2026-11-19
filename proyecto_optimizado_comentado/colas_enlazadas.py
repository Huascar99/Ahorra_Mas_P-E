# ==============================================================================
# MÓDULO: colas_enlazadas.py (100% Estructurado / Sin Clases ni POO)
# Implementa una Cola Enlazada FIFO (First-In, First-Out) usando diccionarios
# para representar cada nodo {"dato": valor, "siguiente": nodo_o_None} y la
# cabecera de la cola {"frente": None, "final": None, "tamano": 0}.
# ==============================================================================


# ==============================================================================
# FUNCIÓN: crear_nodo
# - QUÉ HACE: Crea un diccionario con dos claves: `"dato"` (el valor a guardar)
#   y `"siguiente"` (inicializado en `None` como puntero al próximo nodo).
# - POR QUÉ LO HACE: Para representar un nodo de memoria enlazada de forma
#   procedimental sin necesidad de declarar una clase `class Nodo`.
# - PARA QUÉ SIRVE: Para encapsular cada elemento que entra a la cola enlazada.
# ==============================================================================
def crear_nodo(dato):
    return {"dato": dato, "siguiente": None}


# ==============================================================================
# FUNCIÓN: crear_cola
# - QUÉ HACE: Crea y retorna el diccionario que controla la cola enlazada con
#   sus punteros `"frente"` y `"final"` en `None` y su `"tamano"` en `0`.
# - POR QUÉ LO HACE: Porque una cola enlazada eficiente necesita referencias
#   tanto al primer nodo (para desencolar en `O(1)`) como al último nodo
#   (para encolar en `O(1)`).
# - PARA QUÉ SIRVE: Para inicializar una nueva cola vacía lista para operar.
# ==============================================================================
def crear_cola():
    return {"frente": None, "final": None, "tamano": 0}


# ==============================================================================
# FUNCIÓN: esta_vacia
# - QUÉ HACE: Verifica si el puntero `"frente"` de la cola es `None`.
# - POR QUÉ LO HACE: Porque si no hay nodo al frente, significa que la cola no
#   contiene ningún elemento actualmente.
# - PARA QUÉ SIRVE: Para validar antes de desencolar o consultar elementos y
#   evitar errores de acceso a `None`.
# ==============================================================================
def esta_vacia(cola):
    return cola["frente"] is None


# ==============================================================================
# FUNCIÓN: encolar
# - QUÉ HACE: Crea un nuevo nodo con `dato` y lo enlaza al `"final"` de la cola
#   (o lo asigna tanto a `"frente"` como a `"final"` si la cola estaba vacía),
#   incrementando el `"tamano"` en 1.
# - POR QUÉ LO HACE: Porque en una estructura FIFO (Primero en Entrar, Primero
#   en Salir) los nuevos elementos siempre se forman al final de la fila.
# - PARA QUÉ SIRVE: Para agregar transacciones o solicitudes pendientes a la
#   cola en tiempo constante `O(1)`.
# ==============================================================================
def encolar(cola, dato):
    nuevo_nodo = crear_nodo(dato)
    if esta_vacia(cola):
        cola["frente"] = nuevo_nodo
        cola["final"] = nuevo_nodo
    else:
        cola["final"]["siguiente"] = nuevo_nodo
        cola["final"] = nuevo_nodo

    cola["tamano"] += 1
    return True


# ==============================================================================
# FUNCIÓN: desencolar
# - QUÉ HACE: Extrae y devuelve el `"dato"` del nodo ubicado en el `"frente"`
#   de la cola, avanza el puntero `"frente"` al nodo `"siguiente"` y reduce el
#   `"tamano"` en 1.
# - POR QUÉ LO HACE: Para atender los elementos en estricto orden de llegada
#   (FIFO); si al extraer el elemento la cola queda vacía, también limpia el
#   puntero `"final"`.
# - PARA QUÉ SIRVE: Para procesar y retirar el elemento más antiguo de la cola.
# ==============================================================================
def desencolar(cola):
    if esta_vacia(cola):
        return None

    dato = cola["frente"]["dato"]
    cola["frente"] = cola["frente"]["siguiente"]

    if cola["frente"] is None:
        cola["final"] = None

    cola["tamano"] -= 1
    return dato


# ==============================================================================
# FUNCIÓN: consultar_frente
# - QUÉ HACE: Retorna el dato almacenado en el primer nodo (`"frente"`) sin
#   eliminarlo de la cola.
# - POR QUÉ LO HACE: Para permitir inspeccionar cuál es el próximo elemento a
#   ser atendido sin alterar el estado de la estructura (operación Peek).
# - PARA QUÉ SIRVE: Para ver el primer elemento en espera.
# ==============================================================================
def consultar_frente(cola):
    return None if esta_vacia(cola) else cola["frente"]["dato"]


# ==============================================================================
# FUNCIÓN: consultar_final
# - QUÉ HACE: Retorna el dato almacenado en el último nodo (`"final"`) sin
#   eliminarlo de la cola.
# - POR QUÉ LO HACE: Aprovecha el puntero `"final"` para consultar en tiempo
#   constante `O(1)` el último elemento ingresado.
# - PARA QUÉ SIRVE: Para verificar cuál fue el registro más reciente agregado
#   a la cola.
# ==============================================================================
def consultar_final(cola):
    return None if esta_vacia(cola) else cola["final"]["dato"]


# ==============================================================================
# FUNCIÓN: cantidad_cola
# - QUÉ HACE: Devuelve el valor entero del contador `"tamano"` de la cola.
# - POR QUÉ LO HACE: Porque llevar un contador incremental evita tener que
#   recorrer todos los nodos enlazados cada vez que se desea saber la longitud.
# - PARA QUÉ SIRVE: Para conocer instantáneamente cuántos elementos hay en cola.
# ==============================================================================
def cantidad_cola(cola):
    return cola["tamano"]


# ==============================================================================
# FUNCIÓN: mostrar_cola
# - QUÉ HACE: Recorre los nodos desde `"frente"` siguiendo los enlaces
#   `"siguiente"` hasta llegar a `None` y devuelve una lista con los datos.
# - POR QUÉ LO HACE: Para convertir la cadena de nodos enlazados en una lista
#   estándar que pueda visualizarse sin destruir ni desencolar los nodos.
# - PARA QUÉ SIRVE: Para inspeccionar todos los elementos actuales de la cola.
# ==============================================================================
def mostrar_cola(cola):
    elementos = []
    actual = cola["frente"]
    while actual is not None:
        elementos.append(actual["dato"])
        actual = actual["siguiente"]
    return elementos


# ==============================================================================
# FUNCIÓN: procesar_todos
# - QUÉ HACE: Desencola uno por uno todos los elementos hasta que la cola
#   quede vacía y los retorna en una lista en el orden en que fueron atendidos.
# - POR QUÉ LO HACE: Para vaciar y procesar por lotes todas las operaciones
#   pendientes respetando el orden FIFO.
# - PARA QUÉ SIRVE: Para ejecutar el vaciado activo de toda la cola de trabajo.
# ==============================================================================
def procesar_todos(cola):
    procesados = []
    while not esta_vacia(cola):
        procesados.append(desencolar(cola))
    return procesados


# ==============================================================================
# FUNCIÓN: limpiar_cola
# - QUÉ HACE: Reinicia los punteros `"frente"` y `"final"` a `None` y el
#   `"tamano"` a `0`.
# - POR QUÉ LO HACE: Porque al eliminar las referencias al primer y último
#   nodo, el recolector de basura de Python libera automáticamente toda la
#   cadena de nodos en memoria en tiempo `O(1)`.
# - PARA QUÉ SIRVE: Para vaciar instantáneamente la cola sin recorrerla.
# ==============================================================================
def limpiar_cola(cola):
    cola["frente"] = None
    cola["final"] = None
    cola["tamano"] = 0

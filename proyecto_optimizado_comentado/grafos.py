from collections import deque


# ==============================================================================
# MÓDULO: grafos.py (100% Estructurado / Sin Clases ni POO)
# Implementa un Grafo No Dirigido mediante un diccionario de listas de
# adyacencia: { "VerticeA": ["VerticeB", "VerticeC"], ... }
# ==============================================================================


# ==============================================================================
# FUNCIÓN: crear_grafo
# - QUÉ HACE: Crea y devuelve un diccionario vacío `{}` que actuará como la
#   lista de adyacencia del grafo.
# - POR QUÉ LO HACE: Porque un diccionario donde cada llave es un vértice y
#   su valor es la lista de vértices vecinos es la representación más óptima
#   en memoria y velocidad para grafos sin usar clases.
# - PARA QUÉ SIRVE: Para inicializar un grafo financiero nuevo.
# ==============================================================================
def crear_grafo():
    return {}


# ==============================================================================
# FUNCIÓN: agregar_vertice
# - QUÉ HACE: Si el `nombre` del vértice no existe en el diccionario `grafo`,
#   lo registra con una lista vacía de vecinos `[]` y retorna `True`.
# - POR QUÉ LO HACE: Para asegurar que cada nodo financiero (ej. cuenta, gasto
#   o meta) exista en la estructura antes de conectarlo con otros nodos.
# - PARA QUÉ SIRVE: Para dar de alta nodos o entidades dentro del grafo.
# ==============================================================================
def agregar_vertice(grafo, nombre):
    if nombre not in grafo:
        grafo[nombre] = []
        return True
    return False


# ==============================================================================
# FUNCIÓN: agregar_arista
# - QUÉ HACE: Garantiza que los vértices `origen` y `destino` existan en el
#   grafo y agrega una conexión bidireccional entre ambos evitando duplicados.
# - POR QUÉ LO HACE: Porque en un grafo no dirigido, si A está conectado con B,
#   B también está conectado con A en sus respectivas listas de adyacencia.
# - PARA QUÉ SIRVE: Para relacionar conceptos financieros entre sí (por ejemplo,
#   conectar "Ingresos" con "Ahorro" y "Servicios Básicos").
# ==============================================================================
def agregar_arista(grafo, origen, destino):
    agregar_vertice(grafo, origen)
    agregar_vertice(grafo, destino)

    if destino not in grafo[origen]:
        grafo[origen].append(destino)
    if origen not in grafo[destino]:
        grafo[destino].append(origen)
    return True


# ==============================================================================
# FUNCIÓN: mostrar_grafo
# - QUÉ HACE: Retorna una copia superficial del diccionario de adyacencia con
#   las listas de vecinos copiadas.
# - POR QUÉ LO HACE: Para que quien consulte el grafo pueda leer todas sus
#   conexiones sin riesgo de modificar accidentalmente las listas internas.
# - PARA QUÉ SIRVE: Para inspeccionar el mapa completo de vértices y aristas.
# ==============================================================================
def mostrar_grafo(grafo):
    return {vertice: vecinos.copy() for vertice, vecinos in grafo.items()}


# ==============================================================================
# FUNCIÓN: buscar_conexiones
# - QUÉ HACE: Devuelve una copia de la lista de vecinos directamente conectados
#   al vértice `nombre` (o una lista vacía si el vértice no existe).
# - POR QUÉ LO HACE: Aprovecha la búsqueda `O(1)` de los diccionarios de Python
#   con `.get()` para obtener los nodos adyacentes de inmediato.
# - PARA QUÉ SIRVE: Para saber qué elementos financieros están vinculados
#   directamente con un nodo dado.
# ==============================================================================
def buscar_conexiones(grafo, nombre):
    return grafo.get(nombre, []).copy()


# ==============================================================================
# FUNCIÓN: recorrido_anchura_bfs
# - QUÉ HACE: Recorre el grafo por niveles (Breadth-First Search / Anchura)
#   partiendo del vértice `inicio`, utilizando una cola `deque` y un conjunto
#   `visitados` para no caer en ciclos infinitos.
# - POR QUÉ LO HACE: Porque el algoritmo BFS explora primero todos los vecinos
#   inmediatos (distancia 1), luego los vecinos de los vecinos (distancia 2),
#   encontrando siempre los caminos más cortos en número de saltos.
# - PARA QUÉ SIRVE: Para explorar el grafo financiero por capas de cercanía.
# ==============================================================================
def recorrido_anchura_bfs(grafo, inicio):
    if inicio not in grafo:
        return []

    visitados = {inicio}
    cola = deque([inicio])
    resultado = []

    while cola:
        actual = cola.popleft()
        resultado.append(actual)

        for vecino in grafo[actual]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)

    return resultado


# ==============================================================================
# FUNCIÓN: recorrido_profundidad_dfs
# - QUÉ HACE: Explora el grafo en profundidad (Depth-First Search) desde el
#   vértice `inicio`, avanzando recursivamente por cada camino hasta el fondo
#   antes de retroceder (backtracking).
# - POR QUÉ LO HACE: Utiliza el conjunto `visitados` para recordar por qué
#   nodos ya pasó y evitar bucles cuando el grafo tiene ciclos cerrados.
# - PARA QUÉ SIRVE: Para recorrer cadenas completas de dependencias financieras.
# ==============================================================================
def recorrido_profundidad_dfs(grafo, inicio, visitados=None):
    if inicio not in grafo:
        return []

    if visitados is None:
        visitados = set()

    visitados.add(inicio)
    resultado = [inicio]

    for vecino in grafo[inicio]:
        if vecino not in visitados:
            resultado.extend(recorrido_profundidad_dfs(grafo, vecino, visitados))

    return resultado


# ==============================================================================
# FUNCIÓN: eliminar_arista
# - QUÉ HACE: Remueve el enlace entre `origen` y `destino` en ambas listas de
#   adyacencia si la conexión existe.
# - POR QUÉ LO HACE: Para desconectar dos vértices manteniendo ambos nodos
#   vivos dentro del grafo.
# - PARA QUÉ SIRVE: Para romper una relación entre dos categorías financieras.
# ==============================================================================
def eliminar_arista(grafo, origen, destino):
    if origen not in grafo or destino not in grafo[origen]:
        return False

    grafo[origen].remove(destino)
    grafo[destino].remove(origen)
    return True


# ==============================================================================
# FUNCIÓN: eliminar_vertice
# - QUÉ HACE: Elimina todas las referencias al vértice `nombre` en las listas
#   de vecinos de los demás nodos y finalmente borra la clave `nombre` del grafo.
# - POR QUÉ LO HACE: Porque si borráramos el vértice sin limpiar las listas de
#   sus vecinos, quedarían aristas colgantes apuntando a un nodo inexistente.
# - PARA QUÉ SIRVE: Para dar de baja completamente un nodo y todas sus aristas.
# ==============================================================================
def eliminar_vertice(grafo, nombre):
    if nombre not in grafo:
        return False

    for vecinos in grafo.values():
        if nombre in vecinos:
            vecinos.remove(nombre)

    del grafo[nombre]
    return True


# ==============================================================================
# FUNCIÓN: cantidad_vertices
# - QUÉ HACE: Retorna el número total de vértices registrados en el grafo.
# - POR QUÉ LO HACE: Cada llave del diccionario de adyacencia corresponde a un
#   único vértice.
# - PARA QUÉ SIRVE: Para conocer el orden (cantidad de nodos) del grafo.
# ==============================================================================
def cantidad_vertices(grafo):
    return len(grafo)


# ==============================================================================
# FUNCIÓN: cantidad_aristas
# - QUÉ HACE: Suma la longitud de todas las listas de vecinos y divide el
#   resultado entre 2 (`// 2`).
# - POR QUÉ LO HACE: Porque en un grafo no dirigido cada arista se guarda dos
#   veces (una en el origen y otra en el destino), según el Lema del Apretón
#   de Manos.
# - PARA QUÉ SIRVE: Para conocer el número exacto de conexiones únicas en el grafo.
# ==============================================================================
def cantidad_aristas(grafo):
    return sum(len(vecinos) for vecinos in grafo.values()) // 2

from collections import deque


def crear_grafo():
    return {}


def agregar_vertice(grafo, nombre):
    if nombre not in grafo:
        grafo[nombre] = []
        return True
    return False


def agregar_arista(grafo, origen, destino):
    agregar_vertice(grafo, origen)
    agregar_vertice(grafo, destino)

    if destino not in grafo[origen]:
        grafo[origen].append(destino)
    if origen not in grafo[destino]:
        grafo[destino].append(origen)
    return True


def mostrar_grafo(grafo):
    return {vertice: vecinos.copy() for vertice, vecinos in grafo.items()}


def buscar_conexiones(grafo, nombre):
    return grafo.get(nombre, []).copy()


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


def eliminar_arista(grafo, origen, destino):
    if origen not in grafo or destino not in grafo[origen]:
        return False

    grafo[origen].remove(destino)
    grafo[destino].remove(origen)
    return True


def eliminar_vertice(grafo, nombre):
    if nombre not in grafo:
        return False

    for vecinos in grafo.values():
        if nombre in vecinos:
            vecinos.remove(nombre)

    del grafo[nombre]
    return True


def cantidad_vertices(grafo):
    return len(grafo)


def cantidad_aristas(grafo):
    return sum(len(vecinos) for vecinos in grafo.values()) // 2

def crear_nodo_arbol(nombre):
    return {"nombre": nombre, "hijos": []}


def crear_arbol_financiero(raiz="Finanzas personales"):
    return crear_nodo_arbol(raiz)


def buscar_nodo(nodo_actual, nombre):
    if nodo_actual is None:
        return None

    if nodo_actual["nombre"].lower() == nombre.lower():
        return nodo_actual

    for hijo in nodo_actual["hijos"]:
        encontrado = buscar_nodo(hijo, nombre)
        if encontrado is not None:
            return encontrado

    return None


def agregar_categoria(raiz, padre, nombre):
    nodo_padre = buscar_nodo(raiz, padre)
    if nodo_padre is None or buscar_nodo(raiz, nombre) is not None:
        return False

    nodo_padre["hijos"].append(crear_nodo_arbol(nombre))
    return True


def mostrar_arbol(nodo_actual, nivel=0):
    if nodo_actual is None:
        return []

    resultado = ["    " * nivel + nodo_actual["nombre"]]
    for hijo in nodo_actual["hijos"]:
        resultado.extend(mostrar_arbol(hijo, nivel + 1))
    return resultado


def categorias_principales(raiz):
    return [hijo["nombre"] for hijo in raiz["hijos"]]


def obtener_subcategorias(raiz, nombre):
    nodo = buscar_nodo(raiz, nombre)
    if nodo is None:
        return []
    return [hijo["nombre"] for hijo in nodo["hijos"]]


def eliminar_categoria(nodo_actual, nombre):
    for hijo in nodo_actual["hijos"]:
        if hijo["nombre"].lower() == nombre.lower():
            nodo_actual["hijos"].remove(hijo)
            return True
        if eliminar_categoria(hijo, nombre):
            return True
    return False


def contar_nodos(nodo_actual):
    if nodo_actual is None:
        return 0
    return 1 + sum(contar_nodos(hijo) for hijo in nodo_actual["hijos"])


def recorrido_profundidad(raiz):
    return mostrar_arbol(raiz)

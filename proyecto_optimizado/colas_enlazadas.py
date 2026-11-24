def crear_nodo(dato):
    return {"dato": dato, "siguiente": None}


def crear_cola():
    return {"frente": None, "final": None, "tamano": 0}


def esta_vacia(cola):
    return cola["frente"] is None


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


def desencolar(cola):
    if esta_vacia(cola):
        return None

    dato = cola["frente"]["dato"]
    cola["frente"] = cola["frente"]["siguiente"]

    if cola["frente"] is None:
        cola["final"] = None

    cola["tamano"] -= 1
    return dato


def consultar_frente(cola):
    return None if esta_vacia(cola) else cola["frente"]["dato"]


def consultar_final(cola):
    return None if esta_vacia(cola) else cola["final"]["dato"]


def cantidad_cola(cola):
    return cola["tamano"]


def mostrar_cola(cola):
    elementos = []
    actual = cola["frente"]
    while actual is not None:
        elementos.append(actual["dato"])
        actual = actual["siguiente"]
    return elementos


def procesar_todos(cola):
    procesados = []
    while not esta_vacia(cola):
        procesados.append(desencolar(cola))
    return procesados


def limpiar_cola(cola):
    cola["frente"] = None
    cola["final"] = None
    cola["tamano"] = 0
